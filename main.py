from fastapi import FastAPI, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html

from config import connect_to_mongo, close_mongo_connection, get_database
from controller import router as imovel_router
from models import Imovel

app = FastAPI(
    title="Mongo DB Atlas API",
    description="API para gerenciamento de usuários",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url=None,
    redoc_url=None,
    contact={
        "name": "Grupo 4 do Setimo semestre",
        "email": "caiopecellin@gmail.com",
        "users": "Ana Paula, Caio Costa, Vinicius Martins"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ],
)

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    connect_to_mongo()
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()
    print("Disconnected from the MongoDB database!")

@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get("/docs", tags=["Redirect"], include_in_schema=False)
async def get_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Swagger UI"
    )

@app.get("/openapi.json", tags=["Redirect"], include_in_schema=False)
async def get_openapi():
    return get_swagger_ui(
        title="Mongo DB Atlas API",
        version="1.0.0",
        description="API para gerenciamento de imoveis",
        routes=app.routes,
    )

app.include_router(imovel_router, prefix="/api", tags=["imoveis"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
