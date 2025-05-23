from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Request

from helpers.Dependency import get_session
from helpers.Logging import get_logger
from helpers.OwnerHelper import update_owner_data
from orm.Owner import Owner

router = APIRouter(prefix="/owner", tags=["Owner"])
logger = get_logger(__name__)


@router.get("/")
async def get_owners(session: AsyncSession = Depends(get_session)):
    statement = select(Owner)
    results = await session.exec(statement)
    owners = results.all()

    logger.info(f"Showing all the owners data")
    return owners


# {
#     "Name": "<NAME>",
#     "Age": 0
# }
@router.get("/{owner_id}")
async def get_owner(owner_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Owner).where(Owner.owner_id == owner_id)
    owner_data = await session.exec(query).first()

    if not owner_data:
        logger.info(f"Owner {owner_id} not found")
        raise HTTPException(status_code=404, detail="There is no Owner with this ID")

    else:
        logger.info(f"Showing owner {owner_id} data")
        return owner_data

@router.post("/")
async def add_owner(request: Request, session: AsyncSession = Depends(get_session)):
    #Extracting Data
    data = await request.json()
    owner_name = data["Name"]
    age = data["Age"]

    #Adding Data
    owner = await session.merge(Owner(owner_name=owner_name, age=age))
    await session.commit()

    #Returning Data
    owner_id = await owner.awaitable_attrs.owner_id
    logger.info(f"Owner {owner_id} added")

    return {"owner_id": owner_id}


@router.put("/{owner_id}")
async def update_owner(request: Request, owner_id: int, db: AsyncSession = Depends(get_session)):
    data = await request.json()

    owner_name = data.get("Name", False)
    age = data.get("Age", False)

    if owner_name and age:
        owner = update_owner_data(db, owner_id=owner_id, owner_name=owner_name, age=age)
        logger.info(f"Owner {owner_id} updated: {owner}")
        return owner

    elif owner_name:
        owner = update_owner_data(db, owner_id=owner_id, owner_name=owner_name)
        logger.info(f"Owner {owner_id} updated: {owner}")
        return owner

    elif age:
        owner = update_owner_data(db, owner_id=owner_id, age=age)
        logger.info(f"Owner {owner_id} updated: {owner}")
        return owner

    else:
        raise HTTPException(status_code=404, detail="There is no Owner with this ID")


@router.delete("/{owner_id}")
async def delete_owner(owner_id: int, db: AsyncSession = Depends(get_session)):

    try:
        statement = select(Owner).where(Owner.owner_id == owner_id)
        result = await db.exec(statement)
        owner = result.first()

        if owner:
            await db.delete(owner)
            await db.commit()

        logger.info(f"Owner {owner_id} deleted")
        return {"This owner ID got deleted from Database": owner_id}

    except AttributeError:
        logger.info(f"Owner {owner_id} not found")
        return {"No owner with this name": owner_id}