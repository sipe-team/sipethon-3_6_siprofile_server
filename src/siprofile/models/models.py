from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class BaseEntity(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class RequestCreateUser(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    password: Optional[str] = None


class RequestUpdateUser(BaseModel):
    user_id: str
    name: Optional[str] = None
    password: Optional[str] = None
    profile_image: Optional[str] = None


class RequestDeleteUser(BaseModel):
    user_id: str


class RequestGetUser(BaseModel):
    user_id: str


class RequestCreateCard(BaseModel):
    user_id: str
    name: str
    company: str
    job: str
    labels: List[str]
    files: Optional[List[str]] = None
    link: Optional[str] = None


class RequestUpdateCard(BaseModel):
    card_id: str
    name: Optional[str] = None
    job: Optional[str] = None
    labels: Optional[List[str]] = None
    files: Optional[List[str]] = None
    link: Optional[str] = None


class RequestDeleteCard(BaseModel):
    card_id: str


class RequestGetCard(BaseModel):
    card_id: str


class RequestEnableCard(BaseModel):
    card_id: str


class RequestDisableCard(BaseModel):
    card_id: str


class RequestListCards(BaseModel):
    job: Optional[str] = None
    state: Optional[str] = None
    labels: Optional[List[str]] = None
    user_id: Optional[str] = None


class RequestUpdateFile(BaseModel):
    file_id: str
    reference: Optional[Dict[str, str]] = None


class User(BaseEntity):
    user_id: str
    name: Optional[str] = None
    email: EmailStr
    password: Optional[str] = None
    auth_type: str = "LOCAL"
    profile_image: Optional[str] = None
    last_accessed_at: Optional[datetime] = None


class Card(BaseEntity):
    user_id: str
    name: str
    company: str
    job: str
    state: str = "ACTIVE"
    labels: List[str]
    files: Optional[List[str]] = None
    link: Optional[str] = None


class File(BaseEntity):
    file_id: str
    name: str
    file_type: str
    download_url: str
    state: str
    reference: Dict[str, str]
    user_id: str
