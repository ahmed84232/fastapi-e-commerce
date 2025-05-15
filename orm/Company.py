from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import SQLModel, Relationship, Field
from typing import Optional


class Company(AsyncAttrs, SQLModel, table=True):
    company_id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(max_length=50)
    company_employees: int = Field(default=0)
    owner_id: int = Field(foreign_key="owner.owner_id")

    owner: "Owner" = Relationship(back_populates="company")
