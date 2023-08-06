from pymongo import ReturnDocument
from .base_model import BaseModel
from .fields import StringField, IntField
from ..db import db
from ..errors import IntegrityError


class Counter(BaseModel):
    """
    Counter offers an easy way of achieving SQL database style sequences that MongoDB
    doesn't have built in.

    """

    COLLECTION = "counters"
    KEY_FIELD = "key"

    key = StringField(unique=True)
    counter = IntField(default=1)

    @classmethod
    async def get(cls, key: str) -> "Counter":
        _db = await db()
        coll = _db.meta.conn[cls.collection]
        result = await coll.find_one_and_update(
            {"key": key},
            {"$inc": {"counter": 1}},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        return cls(result)

    @classmethod
    async def get_counter(cls, key: str) -> int:
        cnt = await cls.get(key)
        assert cnt.counter is not None
        return cnt.counter

    async def next(self) -> "Counter":
        if not self.key:
            raise IntegrityError("counter key is not initialised")
        return await self.__class__.get(self.key)

    async def drop(self) -> None:
        _db = await db()
        coll = _db.meta.conn[self.collection]
        await coll.delete_one({"_id": self.id})
