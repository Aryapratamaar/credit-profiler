from pydantic import BaseModel, Field

class RegisterIn(BaseModel):
    uid: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_\-]+$")
    name: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=4)

class UserPublic(BaseModel):
    uid: str
    name: str

class RegisterOut(BaseModel):
    ok: bool
    user: UserPublic

class LoginIn(BaseModel):
    uid: str
    password: str

class LoginOut(BaseModel):
    accessToken: str
    user: UserPublic
    
