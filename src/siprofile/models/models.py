from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime


class BaseEntity(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class User(BaseEntity):
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
    state: str = "DEACTIVE"
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
