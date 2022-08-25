import uvicorn
from fastapi import FastAPI

# Routers
from routers.sqs_receiver import sqs_receiver_router

app = FastAPI(title='worker', docs_url=None, openapi_url=None)

app.include_router(
    sqs_receiver_router,
    tags=["sqs_receiver"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=False, port=8080)
