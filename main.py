import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from MiddleWare import LoggingMiddleware
from routers.CompanyAPI import router as company_router
from routers.OwnerAPI import router as owner_router

app = FastAPI()
app.include_router(owner_router)

app.include_router(company_router)
app.add_middleware(BaseHTTPMiddleware, dispatch=LoggingMiddleware())


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
