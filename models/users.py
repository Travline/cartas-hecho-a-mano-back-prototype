from uuid import UUID
from datetime import datetime, timezone 
from typing import Optional
from sqlmodel import SQLModel, Field
import uuid6
from pydantic import EmailStr, field_validator, BaseModel

class UserBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    mail: EmailStr = Field(unique=True, index=True)

class UserLogin(BaseModel):
    mail: EmailStr
    pwd: str

class UserCreate(UserBase):
    pwd: str

class User(UserBase, table=True):
    __tablename__ = "users"
    user_id: UUID = Field(default_factory=uuid6.uuid7, primary_key=True, nullable=False)
    pwd: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        default=None,
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"}
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str):
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Name cannot be empty")
        return cleaned

class UserRead(UserBase):
    user_id: UUID
    is_active: bool
    created_at: datetime