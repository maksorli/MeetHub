
from pydantic import BaseModel, EmailStr
from typing import Optional


class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    gender: str
    longitude: Optional[float] = None
    latitude: Optional[float] = None