from motor import motor_asyncio

from ecommerce_api.settings import MONGODB_URL

client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.Users
collection = database.users


async def fetch_one(text: str):
    document = await collection.find_one({"text": text})
    return document


async def fetch_all(text: str):
    documents = []
    cursor = collection.find({})
    # async for doc in cursor:
    #     documents.append(1)
    return documents


async def create(text: str):
    document = text
    result = await collection.insert_one(document)
    return document


async def update(par1, par2):
    await collection.update_one({"title": par1}, {"$set": {
        "val": par2
    }})
    document = await collection.find_one({"title": par1})
    return document


async def remove(par1):
    await collection.delete_one({"title": par1})
    return True
