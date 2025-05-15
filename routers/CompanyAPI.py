from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.requests import Request
from helpers.CompanyHelper import update_company_data
from helpers.Dependency import get_session
from helpers.Logging import get_logger
from orm.Company import Company

router = APIRouter(prefix="/company", tags=["Company"])
logger = get_logger(__name__)


@router.get("/")
async def get_companies(session: AsyncSession = Depends(get_session)):
    statement = select(Company)
    result = await session.exec(statement)
    companies = result.all()

    logger.info(f"Showing companies")
    return companies


@router.get("/{company_id}")
async def get_company(company_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Company).where(Company.company_id == company_id)
    result = await session.exec(query)
    company: Company = result.first()

    if not company:
        logger.info(f"Company {company_id} not found")
        raise HTTPException(status_code=404, detail="There is no Company with this ID")

    else:
        logger.info(f"Company {company_id} found")
        return {"Message": f"Name is: {await company.awaitable_attrs.company_name}"}

# {
#     "Name": "<COMPANY>",
#     "Employees": 0,
#     "OwnerID": 0
# }

@router.post("/")
async def add_company(request: Request, session: AsyncSession = Depends(get_session)):
    data = await request.json()

    company_name = data["Name"]
    employees = data["Employees"]
    company_owner = data["OwnerID"]

    company = Company(
        company_name=company_name,
        company_employees=employees,
        owner_id=company_owner
    )

    session.add(company)
    await session.commit()

    company_id = company.awaitable_attrs.company_id
    logger.info(f"Company {company_id} added")

    return {"company_id": company_id}


@router.put("/{company_id}")
async def update_company(request: Request, company_id: int, db: AsyncSession = Depends(get_session)):
    data = await request.json()

    company_name = data.get('Name', False)
    company_employees = data.get('Employees', False)
    owner_id = data.get('OwnerID', False)

    if company_name and company_employees and owner_id:

        company = update_company_data(
            db,
            company_id=company_id,
            company_name=company_name,
            company_employees=company_employees,
            owner_id=owner_id
        )

        logger.info(f"Company {company_id} updated")
        return company

    elif company_name:
        company = update_company_data(db, company_id=company_id, company_name=company_name)
        logger.info(f"Company {company_id} updated")
        return company

    elif company_employees:
        company = update_company_data(db, company_id=company_id, company_employees=company_employees)
        logger.info(f"Company {company_id} updated")
        return company

    elif owner_id:
        company = update_company_data(db, company_id=company_id, owner_id=owner_id)
        logger.info(f"Company {company_id} updated")
        return company

    else:
        logger.info(f"Company {company_id} not found")
        raise HTTPException(status_code=404, detail="There is no company with that ID...")


@router.delete("/{company_id}")
async def delete_company(company_id: int, db: AsyncSession = Depends(get_session)):
    try:
        statement = select(Company).where(Company.company_id == company_id)
        result = await db.exec(statement)
        company = result.first()

        if company:
            await db.delete(company)
            await db.commit()

        logger.info(f"Company {company_id} deleted")
        return {"This company ID got deleted from Database": company_id}

    except AttributeError:
        logger.info(f"Company {company_id} not found")
        return {"No company with this ID": company_id}

