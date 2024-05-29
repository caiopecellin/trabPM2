import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from config import connect_to_mongo, close_mongo_connection, get_database
from controller import router as imovel_router
from bson import ObjectId
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Mongo DB Atlas API",
              description="API para gerenciamento de usuários",
              version="1.0.0")

templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    connect_to_mongo()
    logger.info("Connected to the MongoDB database!")

@app.on_event("shutdown")
async def shutdown_event():
    close_mongo_connection()
    logger.info("Disconnected from the MongoDB database!")

@app.get("/", tags=["Redirect"], include_in_schema=False)
async def redirect_to_docs():
    return {"message": "Welcome to the MongoDB Atlas API"}

app.include_router(imovel_router, prefix="/api", tags=["imoveis"])

@app.get("/imoveis/", response_class=JSONResponse)
async def read_root(request: Request, db=Depends(get_database)):
    try:
        imoveis = await db["db_imoveis_sp"].imoveis_sp.find().to_list(100)
        for imovel in imoveis:
            imovel["_id"] = str(imovel["_id"])
        return imoveis
    except Exception as e:
        logger.error(f"Error fetching imoveis: {e}")
        return {"error": "Internal server error"}, 500

@app.get("/imoveis/{imovel_id}", response_class=JSONResponse)
async def read_imovel(request: Request, imovel_id: str, db=Depends(get_database)):
    try:
        imovel = await db["db_imoveis_sp"].imoveis_sp.find_one({"_id": ObjectId(imovel_id)})
        if imovel:
            imovel["_id"] = str(imovel["_id"])
            return imovel
        else:
            return {"message": "Imovel not found"}, 404
    except Exception as e:
        logger.error(f"Error fetching imovel: {e}")
        return {"error": "Internal server error"}, 500

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
