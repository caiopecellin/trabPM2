# main.py

import asyncio
from teste import mongo_db

async def create_document():
    document = {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "age": 30
    }
    result = await mongo_db.db.imoveis_sp.insert_one(document)
    print(f"Documento inserido com id {result.inserted_id}")

async def read_documents():
    documents = await mongo_db.db.imoveis_sp.find().to_list(length=100)
    for doc in documents:
        print(doc)

async def update_document(doc_id):
    result = await mongo_db.db.imoveis_sp.update_one(
        {"_id": doc_id},
        {"$set": {"age": 31}}
    )
    print(f"Documentos atualizados: {result.modified_count}")

async def delete_document(doc_id):
    result = await mongo_db.db.imoveis_sp.delete_one({"_id": doc_id})
    print(f"Documentos deletados: {result.deleted_count}")

async def main():
    #await create_document()
    await read_documents()
    # Para atualizar ou deletar, substitua `some_doc_id` pelo ObjectId real
    # await update_document(some_doc_id)
    # await delete_document(some_doc_id)

if __name__ == "__main__":
    asyncio.run(main())
