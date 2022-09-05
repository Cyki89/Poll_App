from jose import JWTError, jwt # used for encoding and decoding jwt tokens
from fastapi import HTTPException # used to handle error handling
from passlib.context import CryptContext # used for hashing the password 
from datetime import datetime, timedelta # used to handle expiry time for tokens


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_HOURS = 10


class Auth():
    hasher= CryptContext(schemes=['bcrypt'], deprecated="auto")

    def encode_password(self, password):
        return self.hasher.hash(password)

    def verify_password(self, password, encoded_password):
        return self.hasher.verify(password, encoded_password)

    def encode_token(self, username, scope, exp_time):
        payload = {
            'exp' : datetime.utcnow() + exp_time,
            'iat' : datetime.utcnow(),
            'scope': scope,
            'sub' : username
        }

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def encode_access_token(self, username):
        return self.encode_token(
            username=username,
            scope='access_token',
            exp_time=timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    def encode_refresh_token(self, username):
        return self.encode_token(
            username=username,
            scope='refresh_token',
            exp_time=timedelta(days=0, hours=REFRESH_TOKEN_EXPIRE_HOURS)
        )

    def decode_token(self, token, scope):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if (payload['scope'] != scope):
                raise HTTPException(status_code=401, detail='Scope for the token is invalid')
            return payload['sub']       
        except JWTError as exc:
            raise HTTPException(status_code=401, detail=str(exc))

    def decode_access_token(self, access_token):
        return self.decode_token(access_token, 'access_token')

    def refresh_access_token(self, refresh_token): 
        username = self.decode_token(refresh_token, 'refresh_token')
        return self.encode_access_token(username)