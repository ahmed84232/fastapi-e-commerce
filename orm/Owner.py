from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Relationship, Field
from typing import Optional


class Owner(AsyncAttrs, SQLModel, table=True):
    owner_id: Optional[int] = Field(default=None, primary_key=True)
    owner_name: str = Field(max_length=50)
    age: int = Field()

    company: "Company" = Relationship(back_populates="owner")
