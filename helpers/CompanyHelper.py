from sqlmodel import SQLModel, create_engine, Session, select
from orm.Company import Company
from fastapi import HTTPException

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
SQLModel.metadata.create_all(engine)

def add_company_data(company_name, company_employees, owner_id):
    with Session(engine) as session:
        company = Company(company_name=company_name, company_employees=company_employees, owner_id=owner_id)
        session.add(company)
        session.commit()
        return company.company_id


def update_company_data(company_id: int, company_name=None, company_employees: int = None, owner_id: int = None):
    with Session(engine) as session:
        statement = select(Company).where(Company.company_id == company_id)
        company = session.exec(statement).first()

        if company:
            if company_name:
                company.company_name = company_name
            if company_employees:
                company.company_employees = company_employees
            if owner_id:
                company.owner_id = owner_id
            session.commit()
            return {"Company got updated": company.company_name}

        else:
            raise HTTPException(status_code=404, detail="There is no company with that ID...")


def delete_company_data(company_id: int):
    with Session(engine) as session:
        statement = select(Company).where(Company.company_id == company_id)
        company = session.exec(statement).first()
        if company:
            session.delete(company)
            session.commit()