import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.user = os.getenv("DATABASE_USER")
        self.password = os.getenv("DATABASE_PASSWORD")
        self.cluster_url = os.getenv("DATABASE_HOST")
        self.db_name = os.getenv("DATABASE_NAME")
        self.app_name = os.getenv("DATABASE_APP")
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        connection_string = f"mongodb+srv://{self.user}:{self.password}@{self.cluster_url}/{self.db_name}?retryWrites=true&w=majority&appName={self.app_name}"
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client[os.getenv("DATABASE_MONGO_NAME")]
        self.collection = self.db[os.getenv("DATABASE_MONGO_COLLECTION")]

    async def close(self):
        self.client.close()

# Create an instance of the MongoDB class
mongo_db = MongoDB()
mongo_db.connect()

documents = await mongo_db.collection.find().to_list(length=100)
for doc in documents:
    print(doc)
print(mongo_db.db.collection.find().to_list(length=100))