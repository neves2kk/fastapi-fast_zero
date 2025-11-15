from pydantic import BaseModel, ConfigDict,EmailStr

class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class Database(UserSchema):
    id: int

class Token(BaseModel):
    token_type: str 
    access_token: str