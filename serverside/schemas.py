from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Union
from datetime import datetime


# Organisation Schema
class OrganisationBase(BaseModel):
    title: str

class OrganisationCreate(OrganisationBase):
    owner_id: Union[int, None] = None

class OrganisationUserBase(OrganisationBase):
    uuid: str

class OrganisationDelete(BaseModel):
    pass

class OrganisationRead(OrganisationBase):
    owner_id: Union[int, None] = None
    uuid: str


# User Schema
class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    disabled: Optional[bool] = None


class User(UserBase):
    organisations: List[OrganisationUserBase] = []
    id: int

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    id: int

class UserDelete(UserBase):
    id: int


# Table Schema
class TableBase(BaseModel):
    uuid: str
    title: str

class TableCreate(TableBase):
    pass

class TableRead(TableBase):
    organisation_uuid: str

# List Schema
class ListBase(BaseModel):
    uuid: str
    title: str
    subtitle: str

class ListCreate(ListBase):
    pass

class ListRead(ListBase):
    table_uuid: str

# Task Schema
class TaskBase(BaseModel):
    uuid: str
    title: str
    description: str
    priority: str
    created_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    list_uuid: str

# Subtask Schema
class SubtaskBase(BaseModel):
    uuid: str
    title: str
    description: str
    priority: str
    created_at: datetime

class SubtaskCreate(SubtaskBase):
    pass

class SubtaskRead(SubtaskBase):
    task_uuid: str


# Token
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
