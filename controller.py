from fastapi import APIRouter, HTTPException, Depends
from pymongo import ReturnDocument
from typing import List
from config import get_database
from models import Imovel
from bson import ObjectId
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/imoveis/", response_model=Imovel)
async def create_imovel(imovel: Imovel, db=Depends(get_database)):
    try:
        imovel_dict = imovel.dict(by_alias=True)
        result = await db["db_imoveis_sp"].imoveis_sp.insert_one(imovel_dict)
        if result.inserted_id:
            imovel_dict["_id"] = str(result.inserted_id)
            return imovel_dict
        else:
            raise HTTPException(status_code=400, detail="Imovel not created")
    except Exception as e:
        logger.error(f"Error creating imovel: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/imoveis/", response_model=List[Imovel])
async def get_imoveis(db=Depends(get_database)):
    try:
        imoveis = await db["db_imoveis_sp"].imoveis_sp.find().to_list(100)
        for imovel in imoveis:
            imovel["_id"] = str(imovel["_id"])
        return imoveis
    except Exception as e:
        logger.error(f"Error fetching imoveis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/imoveis/{imovel_id}", response_model=Imovel)
async def get_imovel(imovel_id: str, db=Depends(get_database)):
    try:
        imovel = await db["db_imoveis_sp"].imoveis_sp.find_one({"_id": ObjectId(imovel_id)})
        if imovel:
            imovel["_id"] = str(imovel["_id"])
            return imovel
        else:
            raise HTTPException(status_code=404, detail="Imovel not found")
    except Exception as e:
        logger.error(f"Error fetching imovel: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/imoveis/{imovel_id}", response_model=Imovel)
async def update_imovel(imovel_id: str, imovel: Imovel, db=Depends(get_database)):
    try:
        imovel_dict = imovel.dict(by_alias=True)
        updated_imovel = await db["db_imoveis_sp"].imoveis_sp.find_one_and_update(
            {"_id": ObjectId(imovel_id)},
            {"$set": imovel_dict},
            return_document=ReturnDocument.AFTER
        )
        if updated_imovel:
            updated_imovel["_id"] = str(updated_imovel["_id"])
            return updated_imovel
        else:
            raise HTTPException(status_code=404, detail="Imovel not found")
    except Exception as e:
        logger.error(f"Error updating imovel: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/imoveis/{imovel_id}")
async def delete_imovel(imovel_id: str, db=Depends(get_database)):
    try:
        result = await db["db_imoveis_sp"].imoveis_sp.delete_one({"_id": ObjectId(imovel_id)})
        if result.deleted_count == 1:
            return {"message": "Imovel deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Imovel not found")
    except Exception as e:
        logger.error(f"Error deleting imovel: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
