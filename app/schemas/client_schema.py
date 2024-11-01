from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"


# Схема для создания клиента
class ClientCreate(BaseModel):
    first_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="First name of the client (2-50 characters)",
    )
    last_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        description="Last name of the client (2-50 characters)",
    )
    email: Optional[EmailStr] = Field(
        None, description="User email, must be a valid email address"
    )
    password: Optional[str] = Field(
        None,
        min_length=8,
        max_length=128,
        description="Password for the client (8-128 characters)",
    )
    gender: Optional[GenderEnum] = Field(
        None, description="Gender of the client (Male or Female)"
    )
    longitude: Optional[float] = Field(
        None, ge=-180.0, le=180.0, description="Longitude coordinate (-180 to 180)"
    )
    latitude: Optional[float] = Field(
        None, ge=-90.0, le=90.0, description="Latitude coordinate (-90 to 90)"
    )


class ClientResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderEnum
    # longitude: float
    # latitude: float
    # registration_date: datetime
    daily_likes_count: int
    # last_like_date: datetime

    model_config = {"from_attributes": True}
