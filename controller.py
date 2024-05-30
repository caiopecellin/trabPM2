from fastapi import APIRouter, HTTPException, Depends
from pymongo import ReturnDocument
from typing import List
from config import get_database
from models import Imovel
from bson import ObjectId

router = APIRouter()

@router.post("/imoveis/", response_model=Imovel)
async def create_imovel(imovel: Imovel, db=Depends(get_database)):
    # Remova explicitamente o campo '_id' da solicitação
    imovel_dict = imovel.dict(by_alias=True)
    imovel_dict.pop('_id', None)  # Remove o campo '_id' se estiver presente

    # Insira o imóvel no banco de dados
    result = await db["db_imoveis_sp"].imoveis_sp.insert_one(imovel_dict)
    
    # Atualize o id no dicionário do imóvel apenas se ele existir
    if result.inserted_id:
        imovel_dict["_id"] = str(result.inserted_id)
        return imovel_dict
    raise HTTPException(status_code=400, detail="Imovel não foi criado")

@router.get("/imoveis/", response_model=List[Imovel])
async def get_imoveis(db=Depends(get_database)):
    #Busca todos os imoveis
    imoveis = await db["db_imoveis_sp"].imoveis_sp.find().to_list()
    #Retorna para o cliente
    for imovel in imoveis:
        imovel["_id"] = str(imovel["_id"])
    return imoveis

@router.get("/imoveis/{imovel_id}", response_model=Imovel)
async def get_imovel(imovel_id: str, db=Depends(get_database)):
    # Busque o imovel pelo _id
    imovel = await db["db_imoveis_sp"].imoveis_sp.find_one({"_id": ObjectId(imovel_id)})
    # Retorne o Imovel para o cliente
    if imovel:
        imovel["_id"] = str(imovel["_id"])
        return imovel
    raise HTTPException(status_code=404, detail="Imovel não encontrado")

@router.put("/imoveis/{imovel_id}", response_model=Imovel)
async def update_imovel(imovel_id: str, fields_to_update: dict, db=Depends(get_database)):

    # Verifique se o imóvel com o ID fornecido existe no banco de dados
    existing_imovel = await db["db_imoveis_sp"].imoveis_sp.find_one({"_id": ObjectId(imovel_id)})
    if existing_imovel is None:
        raise HTTPException(status_code=404, detail="Imovel não encontrado")
    
    # Atualize apenas os campos especificados na solicitação
    update_fields = {key: value for key, value in fields_to_update.items()}
    if not update_fields:
        raise HTTPException(status_code=400, detail="Não foram encontrados filtros validos")

    # Atualize o imóvel no banco de dados
    updated_imovel = await db["db_imoveis_sp"].imoveis_sp.find_one_and_update(
        {"_id": ObjectId(imovel_id)},
        {"$set": update_fields},
        return_document=ReturnDocument.AFTER
    )

    # Verifique se o imóvel foi atualizado com sucesso
    if updated_imovel:
        updated_imovel["_id"] = str(updated_imovel["_id"])
        return updated_imovel
    else:
        raise HTTPException(status_code=404, detail="Imovel não encontrado")

@router.delete("/imoveis/{imovel_id}")
async def delete_imovel(imovel_id: str, db=Depends(get_database)):
    # Executa a função de exclusão
    result = await db["db_imoveis_sp"].imoveis_sp.delete_one({"_id": ObjectId(imovel_id)})
    # Retorne a mensagem para o cliente
    if result.deleted_count == 1:
        return {"message": "Imovel apagado com Sucesso!"}
    raise HTTPException(status_code=404, detail="Imovel não encontrado")
