from datetime import datetime
import uvicorn
from bson import ObjectId
from fastapi import Depends, FastAPI, HTTPException, Response, Header, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from db import POLL_DB
from poll_service import models as poll_models
from auth_service import models as auth_models
from auth_service.auth import Auth

QUESTIONNAIRE_COLLECTION = POLL_DB['questionnaires']
QUESTION_COLLECTION = POLL_DB['questions']
VOTING_COLLECTION = POLL_DB['votings']
AUTH_COLLECTION = POLL_DB['users']

auth_handler = Auth()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

COOKIE_EXPIRE_TIME = 24 * 3600 #24H

UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

QUESTIONNAIRE_COLLECTION_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Questionnaire already exists",
)

QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Questionnaire don't exist",
)

QUESTION_COLLECTION_NO_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Question don't exist",
)

USERNAME_EXISTS_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username already exists",
)

ALREADY_VOTED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User voted questionnaire",
)


app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], 
    allow_headers=['Content-Type', 'Authorization']
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    context = []    
    try:
        for error in exc.errors():
            location = error['loc'][-1].replace('_', '')
            context.append({location: error['msg']})
    except AttributeError:
        context = {'body': 'Bad request body'}

    return JSONResponse(
        content=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )




@app.post('/register', response_model=auth_models.UserResponseModel, response_model_exclude=['password'])
async def register_user(form_data:auth_models.UserRegisterModel):
    if await AUTH_COLLECTION.find_one({"username": form_data.username }) != None:
        raise USERNAME_EXISTS_EXCEPTION

    user_data = jsonable_encoder(form_data)
    user_data['password'] = auth_handler.encode_password(user_data['password']) 

    new_user = await AUTH_COLLECTION.insert_one(user_data)
    created_user = await AUTH_COLLECTION.find_one({"_id": new_user.inserted_id})
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content=jsonable_encoder(created_user, custom_encoder={ObjectId: str})
    )


async def get_user(username: str):
    user = await AUTH_COLLECTION.find_one({"username": username})
    if user:
        return auth_models.AuthModel(**user)
    return None


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not auth_handler.verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    username: str = auth_handler.decode_access_token(token)
    user = await get_user(username=username)
    if user is None:
        raise UNAUTHORIZED_EXCEPTION
    return user


@app.post("/login", response_model=auth_models.AccessToken)
async def login(credentials: auth_models.AuthModel):
    user = await authenticate_user(credentials.username, credentials.password)    
    if not user:
        raise UNAUTHORIZED_EXCEPTION
    
    access_token = auth_handler.encode_access_token(user.username)
    refresh_token = auth_handler.encode_refresh_token(user.username)
    response = JSONResponse(content={'access_token': access_token, 'token_type': 'bearer'})
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token,
        httponly=True,
        max_age=COOKIE_EXPIRE_TIME)
    
    return response


@app.post('/logout')
def logout():
    response = Response(status_code=status.HTTP_204_NO_CONTENT)
    response.delete_cookie(key="refresh_token", httponly=True)
    return response


@app.get('/questionnaires', response_model=list[poll_models.Questionnaire])
async def get_questionnaires_list():
    questionnaires = await QUESTIONNAIRE_COLLECTION.find().to_list(length=100)

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content=jsonable_encoder(questionnaires, custom_encoder={ObjectId: str})
    )
    

@app.post('/questionnaires', response_model=poll_models.Questionnaire)
async def create_questionnaire(data: poll_models.Questionnaire):
    if await QUESTIONNAIRE_COLLECTION.find_one({'name': data.name}):
        raise QUESTIONNAIRE_COLLECTION_EXISTS_EXCEPTION

    json_data = jsonable_encoder(data, exclude=['id'])
    new_questionnaire = await QUESTIONNAIRE_COLLECTION.insert_one(json_data)
    created_questionnaire = await QUESTIONNAIRE_COLLECTION.find_one({"_id": new_questionnaire.inserted_id})
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content=jsonable_encoder(created_questionnaire, custom_encoder={ObjectId: str})
    )


@app.get('/questionnaires/{id}', response_model=poll_models.Questionnaire)
async def get_questionnaire(id):
    questionnaire = await QUESTIONNAIRE_COLLECTION.find_one({'_id': ObjectId(id)})
    if not questionnaire:
        raise QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content=jsonable_encoder(questionnaire, custom_encoder={ObjectId: str})
    )


@app.patch('/questionnaires/{id}', response_model=poll_models.Questionnaire)
async def update_questionnaire(id, data:poll_models.QuestionnaireUpdate):
    if not await QUESTIONNAIRE_COLLECTION.find_one({'_id': ObjectId(id)}):
        raise QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION

    await QUESTIONNAIRE_COLLECTION.update_one(
        {"_id": ObjectId(id)}, 
        {'$set': data.dict()}
    )

    updated_questionnaire = await QUESTIONNAIRE_COLLECTION.find_one({"_id": ObjectId(id)})
    
    response = JSONResponse(
        content=jsonable_encoder(updated_questionnaire, custom_encoder={ObjectId: str}),
        status_code=status.HTTP_200_OK
    )

    return response


@app.get('/questionnaires/{id}/questions', response_model=list[poll_models.Question])
async def get_questions(id):
    if not await QUESTIONNAIRE_COLLECTION.find_one({'_id': ObjectId(id)}):
        raise QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION

    questions = await QUESTION_COLLECTION.find({'questionnaire_id': ObjectId(id)}).to_list(length=100)

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content=jsonable_encoder(questions, custom_encoder={ObjectId: str})
    )


@app.post('/questionnaires/{id}/questions', response_model=poll_models.Question)
async def create_question(id, data: poll_models.Question):
    if not await QUESTIONNAIRE_COLLECTION.find_one({'_id': ObjectId(id)}):
        raise QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION

    json_data = jsonable_encoder(data, exclude=['id', 'questionnaire_id'])
    json_data['questionnaire_id'] = ObjectId(id)
    new_question = await QUESTION_COLLECTION.insert_one(json_data)
    created_question = await QUESTION_COLLECTION.find_one({"_id": new_question.inserted_id})
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content=jsonable_encoder(created_question, custom_encoder={ObjectId: str})
    )


@app.get('/questionnaires/{id}/questions/{question_id}', response_model=poll_models.Question)
async def get_question(id, question_id):
    question = await QUESTION_COLLECTION.find_one(
        {'questionnaire_id': ObjectId(id), '_id': ObjectId(question_id)}
    )
    if not question:
        raise QUESTION_COLLECTION_NO_EXISTS_EXCEPTION

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content=jsonable_encoder(question, custom_encoder={ObjectId: str})
    )


@app.patch('/questionnaires/{id}/questions/{question_id}', response_model=poll_models.Question)
async def update_question(id, question_id, data:poll_models.QuestionUpdate):
    question = await QUESTION_COLLECTION.find_one(
        {'questionnaire_id': ObjectId(id), '_id': ObjectId(question_id)}
    )
    if not question:
        raise QUESTION_COLLECTION_NO_EXISTS_EXCEPTION

    await QUESTION_COLLECTION.update_one(
        {"_id": ObjectId(question_id)}, 
        {'$set': data.dict()}
    )

    updated_question = await QUESTION_COLLECTION.find_one({"_id": ObjectId(question_id)})
    
    response = JSONResponse(
        content=jsonable_encoder(updated_question, custom_encoder={ObjectId: str}),
        status_code=status.HTTP_200_OK
    )

    return response


def check_vote(vote, questions):
    for potential_question in questions:
        if vote['question_id'] == potential_question['_id']:
            question = potential_question
            break
    else:
        return False

    for answer in question['answers']:
        if vote['answer_text'] == answer['text'] and vote['answer_id'] == answer['id']:
            return True
    return False


@app.post('/questionnaires/{id}/votings', response_model=list[poll_models.VoteResponse])
async def voting(
    id, 
    votes:list[poll_models.VoteRequest], 
    current_user: auth_models.UserResponseModel = Depends(get_current_user)
):
    if not await QUESTIONNAIRE_COLLECTION.find_one({'_id': ObjectId(id)}):
        raise QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION

    if await VOTING_COLLECTION.find_one({'questionnaire_id': ObjectId(id), 'user_id': current_user.id}):
        raise ALREADY_VOTED_EXCEPTION

    json_votes = jsonable_encoder(votes, custom_encoder={ObjectId: str})
    questions = await QUESTION_COLLECTION.find({'questionnaire_id': ObjectId(id)}).to_list(None)
    json_questions = jsonable_encoder(questions, custom_encoder={ObjectId: str})

    if len(json_questions) != len(json_votes):
        return JSONResponse(
            content='Invalid number of votes',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    invalid_votes = []
    for vote in json_votes:
        if not check_vote(vote, json_questions):
            invalid_votes.append({f'Question {vote["question_id"]}' : 'invalid vote'})
    if invalid_votes:
        return JSONResponse(
            content=invalid_votes,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    votes_to_insert = json_votes.copy()
    for vote_to_insert in votes_to_insert:
        vote_to_insert['questionnaire_id'] = ObjectId(id)
        vote_to_insert['question_id'] = ObjectId(vote_to_insert['question_id'])
        vote_to_insert['user_id'] = current_user.id
        vote_to_insert['date_added'] = datetime.now().strftime("%Y-%m-%d")

    votes_inserted = await VOTING_COLLECTION.insert_many(votes_to_insert)
    votes_results = await VOTING_COLLECTION.aggregate(
        [{"$match": {
                "_id": {"$in": votes_inserted.inserted_ids}
            }
        }]
    ).to_list(None)
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, 
        content=jsonable_encoder(votes_results, custom_encoder={ObjectId: str})
    )


@app.get('/questionnaires/{id}/votings')
async def get_voting_results(id):
    if not await QUESTIONNAIRE_COLLECTION.find_one({'_id': ObjectId(id)}):
        raise QUESTIONNAIRE_COLLECTION_NO_EXISTS_EXCEPTION

    voting_results = await VOTING_COLLECTION.aggregate(
        [
            {
                "$match": {"questionnaire_id":ObjectId(id)}
            },
            {
                "$group": {
                    "_id": {
                        "question_id": "$question_id",
                        "answer_id": "$answer_id",
                        "answer_text": "$answer_text"
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$project" : { 
                    "question_id" : "$_id.question_id", 
                    "answer_id" : "$_id.answer_id", 
                    "answer_text" : "$_id.answer_text", 
                    "_id": False,
                    "count" : True 
                }
            }
        ]
    ).to_list(None)

    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content=jsonable_encoder(voting_results, custom_encoder={ObjectId: str})
    )


'''
[
  {"question_id" : "62a139f558fb1d2c753308ef", "answer_id" : 1, "answer_text": "ans1" },
  {"question_id" : "62a13a1895e636bc6acb6e72", "answer_id" : 1, "answer_text": "ans1" },
  {"question_id" : "62a13fdf477ce9fcb69e1c0c", "answer_id" : 1, "answer_text": "ans1" }
]
'''

# @app.post('/register', response_model=UserResponseModel)
# async def create_record(form_data:UserRegistrationModel):
#     if await AUTH_DB["users"].find_one({"username": form_data.username }) != None:
#         raise USERNAME_EXISTS_EXCEPTION

#     user_data = jsonable_encoder(form_data)
#     user_data['password'] = auth_handler.encode_password(user_data['password']) 

#     new_user = await AUTH_DB["users"].insert_one(user_data)
#     created_user = await AUTH_DB["users"].find_one({"_id": new_user.inserted_id})
    
#     return JSONResponse(
#         status_code=status.HTTP_201_CREATED, 
#         content=jsonable_encoder(created_user, custom_encoder={ObjectId: str})
#     )


# async def get_user(db, username: str):
#     user = await db["users"].find_one({"username": username})
#     if user:
#         return UserInDBModel(**user)


# async def authenticate_user( username: str, password: str):
#     user = await get_user(AUTH_DB, username)
#     if not user:
#         return False
#     if not auth_handler.verify_password(password, user.password):
#         return False
#     return user


# @app.post("/login", response_model=AccessToken)
# async def login(credentials: UserLogin):
#     user = await authenticate_user(credentials.username, credentials.password)    
#     if not user:
#         raise UNAUTHORIZED_EXCEPTION
    
#     access_token = auth_handler.encode_access_token(user.username)
#     refresh_token = auth_handler.encode_refresh_token(user.username)
#     response = JSONResponse(content={'access_token': access_token, 'token_type': 'bearer'})
#     response.set_cookie(
#         key="refresh_token", 
#         value=refresh_token,
#         httponly=True,
#         max_age=COOKIE_EXPIRE_TIME)
#     return response


# @app.post('/logout')
# def refresh_token():
#     response = Response(status_code=status.HTTP_204_NO_CONTENT)
#     response.delete_cookie(key="refresh_token", httponly=True)
#     return response


# @app.post('/refresh', response_model=AccessToken)
# def refresh_token(refresh_token: str | None = Cookie(default=None)):
#     if not refresh_token:
#         raise UNAUTHORIZED_EXCEPTION
#     return {'access_token': auth_handler.refresh_access_token(refresh_token), 'token_type': 'bearer'}


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     username: str = auth_handler.decode_access_token(token)
#     user = await get_user(AUTH_DB, username=username)
#     if user is None:
#         raise UNAUTHORIZED_EXCEPTION
#     return user


# async def get_current_active_user(current_user: UserResponseModel = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.get('/users/me', response_model=UserResponseModel)
# async def read_users_me(current_user: UserResponseModel = Depends(get_current_active_user)):
#     return current_user


# @app.post('/users/update', response_model=UserResponseModel)
# async def update_user_profile(
#     user_data: UserBaseModel,
#     current_user: UserResponseModel = Depends(get_current_active_user),
# ):
#     if current_user.username != user_data.username and await get_user(
#         AUTH_DB, user_data.username) is not None: 
#         raise USERNAME_EXISTS_EXCEPTION

#     await AUTH_DB["users"].update_one(
#         {"username": current_user.username}, 
#         {'$set': user_data.dict()}
#     )

#     response = JSONResponse(
#         content={'detail': 'Success Update'},
#         status_code=status.HTTP_200_OK
#     )

#     return response


# @app.post('/secret')
# def secret_data(current_user: UserResponseModel = Depends(get_current_active_user)):
#     return JSONResponse(content={'message': 'Secret Data'}, status_code=status.HTTP_200_OK)


# @app.get('/notsecret')
# def not_secret_data():
#     return JSONResponse(content={'message': 'Not Secret Data'}, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="127.0.0.1", port=8000, reload=True)