from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from uuid import UUID
import uuid6

class CardImage(SQLModel, table=True):
  __tablename__ = "card_images"
  
  img_id: UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
  card_id: UUID = Field(foreign_key="cards.card_id", ondelete="CASCADE")
  
  card: "Card" = Relationship(back_populates="images")

class Card(SQLModel, table=True):
  __tablename__ = "cards"
  
  card_id: UUID = Field(default_factory=uuid6.uuid7, primary_key=True)
  name: str = Field(index=True)
  description: Optional[str] = Field(default=None)
  is_visible: bool = Field(default=True)

  images: List[CardImage] = Relationship(back_populates="card", cascade_delete=True)


class CardCreate(BaseModel):
  name: str
  description: Optional[str] = None

class CardRead(BaseModel):
  card_id: UUID
  name: str
  description: Optional[str]
  is_visible: bool
  images: List[UUID] = []