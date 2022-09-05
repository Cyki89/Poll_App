from bson import ObjectId
from pydantic import (
    BaseModel, 
    Field,
    EmailStr,
    constr,
)

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


class UserResponseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: CharField
    email: EmailStr | None
    full_name: CharField | None
    disabled: bool = False
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserRegisterModel(BaseModel):
    username: CharField
    password: constr(min_length=4)
    email: EmailStr | None
    full_name: CharField | None
    disabled: bool = False


class AuthModel(BaseModel):
    id: PyObjectId | None = Field(alias="_id")
    username: CharField
    password: constr(min_length=4)


class AccessToken(BaseModel):
    access_token: str
    token_type: str