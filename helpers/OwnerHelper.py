from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from orm.Owner import Owner
from fastapi import HTTPException


async def update_owner_data(db, owner_id: int, owner_name=None, age=None):

    statement = select(Owner).where(Owner.owner_id == owner_id)
    owner: Owner = db.exec(statement).first()

    if owner:

        if owner_name:
            owner.owner_name = owner_name

        if age:
            owner.age = age

        await db.commit()
        return {"Owner got updated": await owner.awaitable_attrs.owner_name}

    else:
        raise HTTPException(status_code=404, detail="There is no owner with that ID...")
