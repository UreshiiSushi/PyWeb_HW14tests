import re
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, validator, EmailStr


class ContactsModel(BaseModel):
    name: str = Field(max_length=50)


class ContactsResponse(ContactsModel):
    id: int

    class Config:
        from_attributes = True


class ContactEmail(BaseModel):
    email: EmailStr


class ContactModel(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(max_length=50)
    phone: str = Field(min_length=12, max_length=20)
    born_date: date
    description: Optional[str] = Field(None, max_length=250)

    @validator("phone")
    def phone_number_must_have_12_digits(cls, phone):
        match = re.match(r"^\+?\d{2,3}\(?\d{2,3}\)?\s?(\d{2,3}\-?){2}\d{2,3}", phone)
        if match is None:
            raise ValueError("Phone number must have more than 12 digits")
        return phone


# Get full list of contacts
class ResponseContactModel(BaseModel):
    id: int = Field(default=1, ge=1)
    name: str = Field(min_length=3, max_length=50)
    lastname: str = Field(min_length=3, max_length=50)
    email: EmailStr
    phone: str = Field(min_length=10, max_length=20)
    born_date: date
    description: Optional[str] = Field(max_length=250)

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
