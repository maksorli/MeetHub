from fastapi import FastAPI

from app.routers import client_router

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "EasyWarehouse  app"}


app.include_router(client_router.router)
