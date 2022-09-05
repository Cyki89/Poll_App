from pydantic import (
    BaseModel, 
    Field,
    EmailStr,
    conlist,
    conint
)
from bson import ObjectId
from datetime import date, datetime


class PyObjectId(ObjectId):
    """ Custom Type for reading MongoDB IDs """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object_id")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CharField(str):
    MIN_LENGTH = 1
    MAX_LENGTH = 255

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not cls.MIN_LENGTH <= len(v) <= cls.MAX_LENGTH:
            raise ValueError("Invalid length")
        return v.replace(' ', '').lower()


class TextField(str):
    MIN_LENGTH = 1

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) < cls.MIN_LENGTH:
            raise ValueError("Invalid length")
        return v


class Questionnaire(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: CharField
    description:TextField
    date_added: date = Field(default_factory=datetime.now().date)
    is_active: bool = True


class QuestionnaireUpdate(BaseModel):
    name: CharField
    description:TextField
    is_active:bool


class Answer(BaseModel):
    id: conint(ge=1)
    text: TextField


class Question(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    text: TextField
    date_added: date = Field(default_factory=datetime.now().date)
    questionnaire_id: PyObjectId | None
    answers: conlist(
        item_type=Answer,
        min_items=2,
        unique_items=True
    )


class QuestionUpdate(BaseModel):
    text: TextField
    answers: conlist(
        item_type=Answer,
        min_items=2,
        unique_items=True
    )


class VoteRequest(BaseModel):
    question_id: PyObjectId 
    answer_id: conint(ge=0)
    answer_text: TextField


class VoteResponse(VoteRequest):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    date_added: date = Field(default_factory=datetime.now().date)
    user_id: PyObjectId
    questionnaire_id: PyObjectId