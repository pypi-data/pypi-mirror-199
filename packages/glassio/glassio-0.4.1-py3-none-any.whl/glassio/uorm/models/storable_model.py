from typing import Coroutine, Dict, Any, Tuple, Optional, Type, List, Callable
from functools import partial
from time import time
from motor.motor_asyncio import AsyncIOMotorCursor
from bson.objectid import ObjectId
from .base_model import BaseModel
from ..db import db, ObjectsCursor, Shard
from ..errors import ModelDestroyed
from glassio import ctx
from glassio.types import MT
from glassio.errors import NotFound
from ..util import resolve_id, save_required


class StorableModel(BaseModel):

    @staticmethod
    async def _db() -> Shard:
        _db = await db()
        return _db.meta

    async def _save_to_db(self) -> None:
        _db = await self._db()
        await _db.save_obj(self)

    async def update(self: MT, data: Dict[str, Any], skip_callback: bool = False, invalidate_cache: bool = True) -> MT:
        for field, descriptor in self._fields.items():
            if (
                field in data
                and not descriptor.rejected
                and field != "_id"
            ):
                self.__dict__[field] = data[field]
        return await self.save(skip_callback=skip_callback, invalidate_cache=invalidate_cache)

    @save_required
    async def db_update(self,
                        update: Dict[str, Any],
                        when: Optional[Dict[str, Any]] = None,
                        reload: bool = True,
                        invalidate_cache: bool = True) -> bool:
        """
        :param update: MongoDB update query
        :param when: filter query. No update will happen if it does not match
        :param reload: Load the new stat into the object (Caution: if you do not do this
                        the next save() will overwrite updated fields)
        :param invalidate_cache: whether to run cache invalidation for the model if the model is changed
        :return: True if the document was updated. Otherwise - False
        """
        _db = await self._db()
        new_data = await _db.find_and_update_obj(self, update, when)
        if invalidate_cache and new_data:
            await self.invalidate()

        if reload and new_data:
            tmp = self.__class__(new_data)
            self._reload_from_model(tmp)

        return bool(new_data)

    async def _delete_from_db(self) -> None:
        _db = await self._db()
        await _db.delete_obj(self)

    async def _refetch_from_db(self: MT) -> Optional[MT]:
        return await self.find_one({"_id": self.id})

    async def reload(self) -> None:
        if self.is_new:
            return
        tmp = await self._refetch_from_db()
        if tmp is None:
            raise ModelDestroyed("model has been deleted from db")
        self._reload_from_model(tmp)

    @classmethod
    def _preprocess_query(cls, query: Dict[str, Any]) -> Dict[str, Any]:
        return query

    @classmethod
    async def find(cls: Type[MT], query: Optional[Dict[str, Any]] = None, **kwargs: Dict[str, Any]) -> ObjectsCursor[MT]:
        if not query:
            query = {}
        _db = await db()
        return _db.meta.get_objs(
            cls, cls.collection, cls._preprocess_query(query), **kwargs
        )

    @classmethod
    async def aggregate(cls,
                  pipeline: List[Dict[str, Any]],
                  query: Optional[Dict[str, Any]] = None,
                  **kwargs: Dict[str, Any]) -> AsyncIOMotorCursor:
        if not query:
            query = {}
        pipeline = [{"$match": cls._preprocess_query(query)}] + pipeline
        _db = await db()
        return _db.meta.get_aggregated(cls.collection, pipeline, **kwargs)

    @classmethod
    async def find_projected(cls,
                       query: Optional[Dict[str, Any]] = None,
                       projection: Tuple[str] = ("_id",),
                       **kwargs: Dict[str, Any]) -> AsyncIOMotorCursor:
        if not query:
            query = {}
        _db = await db()
        return _db.meta.get_objs_projected(
            cls.collection,
            cls._preprocess_query(query),
            projection=projection,
            **kwargs,
        )

    @classmethod
    async def find_one(cls: Type[MT], query: Dict[str, Any], **kwargs: Dict[str, Any]) -> Optional[MT]:
        _db = await db()
        return await _db.meta.get_obj(
            cls, cls.collection, cls._preprocess_query(query), **kwargs
        )

    @classmethod
    async def get(cls: Type[MT],
                  expression: str | ObjectId | None,
                  raise_if_none: Optional[Exception] = None) -> Optional[MT]:
        if expression is None:
            return None

        rexp = resolve_id(expression)
        if isinstance(rexp, ObjectId):
            query = {"_id": rexp}
        else:
            query = {cls.KEY_FIELD: str(rexp)}
        res = await cls.find_one(query)
        if res is None and raise_if_none is not None:
            if isinstance(raise_if_none, Exception):
                raise raise_if_none
            else:
                raise NotFound(f"{cls.__name__} not found")
        return res

    @classmethod
    async def count(cls, query: Optional[Dict[str, Any]] = None) -> int:
        if query is None:
            query = {}
        _db = await db()
        return await _db.meta.count_docs(cls.COLLECTION, query)

    @classmethod
    async def destroy_all(cls) -> None:
        _db = await db()
        await _db.meta.delete_query(cls.collection, cls._preprocess_query({}))

    @classmethod
    async def destroy_many(cls, query: Dict[str, Any]) -> None:
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        _db = await db()
        await _db.meta.delete_query(cls.collection, cls._preprocess_query(query))

    @classmethod
    async def update_many(cls, query: Dict[str, Any], attrs: Dict[str, Any]) -> None:
        # warning: being a faster method than traditional model manipulation,
        # this method doesn't provide any lifecycle callback for independent
        # objects
        _db = await db()
        await _db.meta.update_query(cls.collection, cls._preprocess_query(query), attrs)

    @classmethod
    async def cache_get(cls: Type[MT],
                        expression: str | None,
                        raise_if_none: Optional[Exception] = None) -> Optional[MT]:
        if expression is None:
            return None
        cache_key = f"{cls.collection}.{expression}"
        getter = partial(cls.get, expression, raise_if_none)
        return await cls._cache_get(cache_key, getter)

    @classmethod
    async def _cache_get(cls: Type[MT],
                         cache_key: str,
                         getter: partial[Coroutine[None, None, MT | None]],
                         ctor: Optional[Callable[..., MT]] = None) -> Optional[MT]:
        t1 = time()
        if not ctor:
            ctor = cls

        _db = await db()
        if await _db.l1c.has(cache_key):
            data = await _db.l1c.get(cache_key)
            td = time() - t1
            ctx.log.debug(
                "%s L1 hit %s %.3f secs", _db.l1c.__class__.__name__, cache_key, td
            )
            return ctor(data)

        if await _db.l2c.has(cache_key):
            data = await _db.l2c.get(cache_key)
            await _db.l1c.set(cache_key, data)
            td = time() - t1
            ctx.log.debug(
                "%s L2 hit %s %.3f secs", _db.l2c.__class__.__name__, cache_key, td
            )
            return ctor(data)

        obj = await getter()
        if obj:
            data = obj.to_dict(include_restricted=True)
            await _db.l2c.set(cache_key, data)
            await _db.l1c.set(cache_key, data)

        td = time() - t1
        ctx.log.debug("%s miss %s %.3f secs", _db.l2c.__class__.__name__, cache_key, td)
        return obj

    async def invalidate(self, **kwargs: Dict[str, Any]) -> None:
        for field in self._cache_key_fields:
            value = self._initial_state.get(field)
            if value:
                await self._invalidate(f"{self.collection}.{value}")

    @staticmethod
    async def _invalidate(cache_key: str) -> None:
        _db = await db()
        if await _db.l1c.delete(cache_key):
            ctx.log.debug("%s delete %s", _db.l1c.__class__.__name__, cache_key)
        if await _db.l2c.delete(cache_key):
            ctx.log.debug("%s delete %s", _db.l2c.__class__.__name__, cache_key)
