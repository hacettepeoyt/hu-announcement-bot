import datetime

from motor.motor_asyncio import AsyncIOMotorClient


class DepartmentDatabase:
    CONNECTION_STRING: str
    DB_NAME: str

    def __init__(self, connection_string: str, db_name: str):
        self.CONNECTION_STRING = connection_string
        self.DB_NAME = db_name

    def __fetch_collection(self) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(self.CONNECTION_STRING)
        db = client[self.DB_NAME]
        collection = db['departments']
        return collection

    async def find(self, department_id: str) -> list[dict]:
        collection = self.__fetch_collection()
        document = await collection.find_one({'department_id': department_id})

        if not document:
            await collection.insert_one({
                'department_id': department_id,
                'announcement_list': [],
                'is_active': True
            })
            return []

        return document

    async def update(self, department_id: str, announcement_list: list[dict]) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'department_id': department_id},
                                             {'$set': {'announcement_list': announcement_list}})

    async def toggle_is_active(self, department_id: int) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'department_id': department_id},
                                             [{'$set': {'is_active': {'$not': '$is_active'}}}])


class UserDatabase:
    CONNECTION_STRING: str
    DB_NAME: str

    def __init__(self, connection_string: str, db_name: str):
        self.CONNECTION_STRING = connection_string
        self.DB_NAME = db_name

    def __fetch_collection(self) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(self.CONNECTION_STRING)
        db = client[self.DB_NAME]
        collection = db['users']
        return collection

    async def new_user(self, user_id: int, first_name: str, last_name: str, default_departments: list[str],
                       language: str = "tr", holiday_mode: bool = False, dnd: bool = False) -> dict:
        collection = self.__fetch_collection()
        user = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'departments': default_departments,
            'language': language,
            'dnd': dnd,
            'holiday_mode': holiday_mode
        }
        await collection.insert_one(user)
        return user

    async def find(self, user_id: int) -> dict:
        collection = self.__fetch_collection()
        return await collection.find_one({'user_id': user_id})

    async def find_all(self) -> list[int]:
        user_configs = self.__fetch_collection()
        users_cursor = user_configs.find({})
        user_list = await users_cursor.to_list(None)  # ChatGPT wrote here, I'm not sure why await find() didn't work
        return user_list

    async def toggle_language(self, user_id: int, langauge: str) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'user_id': user_id},
                                             {'$set': {'language': langauge}})

    async def toggle_dnd(self, user_id: int) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'user_id': user_id},
                                             [{'$set': {'dnd': {'$not': '$dnd'}}}])

    async def toggle_holiday_mode(self, user_id: int) -> None:
        collection = self.__fetch_collection()
        await collection.find_one_and_update({'user_id': user_id},
                                             [{'$set': {'holiday_mode': {'$not': '$holiday_mode'}}}])

    async def update_subscriptions(self, user_id: int, departments: list[str]) -> None:
        user_configs = self.__fetch_collection()
        await user_configs.find_one_and_update({'user_id': user_id},
                                               {'$set': {'departments': departments}})

    async def get_subscribers(self, department_name: str) -> list[dict]:
        user_configs = self.__fetch_collection()
        users_cursor = user_configs.find({'departments': department_name, 'holiday_mode': False})
        user_list = await users_cursor.to_list(None)  # ChatGPT wrote here, I'm not sure why await find() didn't work
        return user_list


class FeedbackDatabase:
    CONNECTION_STRING: str
    DB_NAME: str

    def __init__(self, connection_string: str, db_name: str):
        self.CONNECTION_STRING = connection_string
        self.DB_NAME = db_name

    def __fetch_collection(self) -> AsyncIOMotorClient:
        client = AsyncIOMotorClient(self.CONNECTION_STRING)
        db = client[self.DB_NAME]
        collection = db['feedbacks']
        return collection

    async def new_feedback(self, user_id: int, original_message_id: int, message_id: int, message_text: str) -> dict:
        collection = self.__fetch_collection()

        # Message text doesn't have big role in this document, but it could be useful for diagnostic reasons.
        # Therefore, to keep the database lighter, I decided to shorten the text up to 64 chars.
        if len(message_text) > 64:
            message_text = message_text[:64]

        feedback = {
            'user_id': user_id,
            'original_message_id': original_message_id,
            'forwarded_message_id': message_id,
            'message_text': message_text,
            'last_modified': datetime.datetime.now(tz=datetime.timezone.utc)
        }
        await collection.insert_one(feedback)
        return feedback

    async def find_by_message_id(self, forwarded_message_id: int) -> dict:
        collection = self.__fetch_collection()
        return await collection.find_one({'forwarded_message_id': forwarded_message_id})
