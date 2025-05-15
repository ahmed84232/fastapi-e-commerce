from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession

from orm.Company import Company
from fastapi import HTTPException



async def update_company_data(db, company_id: int, company_name=None, company_employees: int = None, owner_id: int = None):
    statement = select(Company).where(Company.company_id == company_id)
    company: Company = await db.exec(statement).first()

    if company:
        if company_name:
            company.company_name = company_name

        if company_employees:
            company.company_employees = company_employees

        if owner_id:
            company.owner_id = owner_id

        await db.commit()
        return {"Company got updated": await company.awaitable_attrs.company_name}

    else:
        raise HTTPException(status_code=404, detail="There is no company with that ID...")
