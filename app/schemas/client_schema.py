from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class GenderEnum(str, Enum):
    male = "Male"
    female = "Female"


class ClientCreate(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="First name of the client (2-50 characters)",
    )
    last_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Last name of the client (2-50 characters)",
    )
    email: EmailStr = Field(
        ..., description="User email, must be a valid email address"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Password for the client (8-128 characters)",
    )
    gender: GenderEnum = Field(..., description="Пол клиента (Male или Female)")
    longitude: float = Field(
        ..., ge=-180.0, le=180.0, description="Longitude coordinate (-180 to 180)"
    )
    latitude: float = Field(
        ..., ge=-90.0, le=90.0, description="Latitude coordinate (-90 to 90)"
    )
