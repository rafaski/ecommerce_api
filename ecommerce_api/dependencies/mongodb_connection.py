from motor import motor_asyncio

from ecommerce_api.settings import MONGODB_URL
from ecommerce_api.schemas import User

client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.Users
collection = database.users


async def get_user(email: str):
    user = await collection.find_one({"email": email})
    return user


async def get_all_users():
    users = []
    cursor = await collection.find({})
    async for user in cursor:
        users.append(User(**user))
    return users


async def create_user(user: User):
    await collection.insert_one(user)
    return user


async def remove_user(email: str):
    await collection.delete_one({"email": email})
