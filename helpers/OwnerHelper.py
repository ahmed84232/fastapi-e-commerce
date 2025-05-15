from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from orm.Owner import Owner
from fastapi import HTTPException, Depends
from helpers.Dependency import get_session

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
SQLModel.metadata.create_all(engine)


def update_owner_data(owner_id: int, owner_name=None, age=None):
    with Session(engine) as session:
        statement = select(Owner).where(Owner.owner_id == owner_id)
        owner = session.exec(statement).first()

        if owner:
            if owner_name:
                owner.owner_name = owner_name
            if age:
                owner.age = age
            session.commit()
            return {"Owner got updated": owner.owner_name}

        else:
            raise HTTPException(status_code=404, detail="There is no owner with that ID...")
