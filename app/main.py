from fastapi import FastAPI

from app.routers import client_router

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Meethub  app"}


app.include_router(client_router.router)

from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Meethub API",
        version="1.0.0",
        description="API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "basicAuth": {"type": "http", "scheme": "basic"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"basicAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
