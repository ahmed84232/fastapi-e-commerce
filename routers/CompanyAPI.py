from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from helpers.CompanyHelper import update_company_data
from helpers.Dependency import get_session
from orm.Company import Company
from MiddleWare import logger

router = APIRouter(prefix="/company", tags=["Company"])


@router.get("/")
async def get_companies(session: AsyncSession = Depends(get_session)):
    statement = select(Company)
    companies = await session.exec(statement)
    companies = companies.all()
    logger.info(f"Showing companies")
    return companies


@router.get("/{company_id}")
async def get_company(company_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Company).where(Company.company_id == company_id)
    company_data = await session.exec(query).first()
    if not company_data:
        logger.info(f"Company {company_id} not found")
        raise HTTPException(status_code=404, detail="There is no Company with this ID")
    else:
        logger.info(f"Company {company_id} found")
        return {"Message": f"Name is: {company_data.company_name}"}


@router.post("/")
async def add_company(request: Request, session: AsyncSession = Depends(get_session)):
    data = await request.json()
    company_name = data["Name"]
    employees = data["Employees"]
    company_owner = data["OwnerID"]
    company = Company(company_name=company_name, company_employees=employees, owner_id=company_owner)
    session.add(company)
    await session.commit()
    company_id = company.company_id
    logger.info(f"Company {company_id} added")

    # {
    #     "Name": "<COMPANY>",
    #     "Employees": 0,
    #     "OwnerID": 0
    # }

    return {"company_id": company_id}


@router.put("/{company_id}")
async def update_company(request: Request, company_id: int):
    data = await request.json()
    try:
        company_name = data["Name"]
    except KeyError:
        company_name = False
        pass

    try:
        company_employees = data["Employees"]
    except KeyError:
        company_employees = False
        pass

    try:
        owner_id = data["OwnerID"]
    except KeyError:
        owner_id = False
        pass

    if company_name and company_employees and owner_id:
        the_update = update_company_data(
            company_id=company_id,
            company_name=company_name,
            company_employees=company_employees,
            owner_id=owner_id
        )
        logger.info(f"Company {company_id} updated")
        return the_update
    elif company_name:
        the_update = update_company_data(company_id=company_id, company_name=company_name)
        logger.info(f"Company {company_id} updated")
        return the_update
    elif company_employees:
        the_update = update_company_data(company_id=company_id, company_employees=company_employees)
        logger.info(f"Company {company_id} updated")
        return the_update
    elif owner_id:
        the_update = update_company_data(company_id=company_id, owner_id=owner_id)
        logger.info(f"Company {company_id} updated")
        return the_update
    else:
        logger.info(f"Company {company_id} not found")
        raise HTTPException(status_code=404, detail="There is no company with that ID...")


@router.delete("/{company_id}")
async def delete_company(company_id: int, session: AsyncSession = Depends(get_session)):
    try:
        statement = select(Company).where(Company.company_id == company_id)
        company = await session.exec(statement).first()
        if company:
            await session.delete(company)
            await session.commit()
        logger.info(f"Company {company_id} deleted")
        return {"This company ID got deleted from Database": company_id}
    except AttributeError:
        logger.info(f"Company {company_id} not found")
        return {"No company with this ID": company_id}

