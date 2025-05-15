import uvicorn
from fastapi import FastAPI, Request
from MiddleWare import logger
from routers.CompanyAPI import router as company_router
from routers.OwnerAPI import router as owner_router
import json

app = FastAPI()
app.include_router(owner_router)

app.include_router(company_router)


@app.middleware("http")
async def requests_middleware(request: Request, call_next):

    headers = {header: value for header, value in request.headers.items()}
    json_headers = json.dumps(headers, indent=2)

    body = await request.body()
    if body:
        content_type = request.headers.get("Content-Type", "")
        if content_type == "application/json":
            try:
                body = json.loads(body)
                json_body = json.dumps(body, indent=2)
                logger.info(f"\n-----FastAPI Request-----\n{request.method} {request.url}\n{json_headers}\n-----Request Body-----\n{json_body}")
            except Exception as e:
                logger.warning(f"Could not decode body: {e}")
        else:
            try:
                body = body.decode("utf-8")
                logger.info(f"\n-----FastAPI Request-----\n{request.method} {request.url}\n{json_headers}\n-----Request Body-----\n{body}")
            except Exception as e:
                logger.warning(f"Could not decode body: {e}")
    else:
        pass

    response = await call_next(request)
    logger.info(f"Response code: {response.status_code}")

    return response

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
