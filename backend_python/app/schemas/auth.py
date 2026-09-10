from typing import Optional
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class UserInfo(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    role: str
    email: Optional[str] = None

class LoginResponse(BaseModel):
    status: str = "success"
    token: str
    user: UserInfo
