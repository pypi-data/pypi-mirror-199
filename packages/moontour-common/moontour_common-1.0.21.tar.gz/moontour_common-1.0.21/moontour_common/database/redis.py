import json
import os
from contextlib import asynccontextmanager
from typing import TypeVar, AsyncContextManager

import redis
import redis.asyncio as asyncio_redis
from redis.commands.json.path import Path

from moontour_common.database.rabbitmq import notify_room
from moontour_common.models import BaseRoom

_RoomType = TypeVar('_RoomType', bound=BaseRoom)

ROOM_KEY_PREFIX = 'room:'

_host = os.getenv('REDIS_HOST', 'redis')
redis_client = redis.Redis(host=_host)
async_redis_client = asyncio_redis.Redis(host=_host)


def get_room_key(room_id: str) -> str:
    return f'{ROOM_KEY_PREFIX}{room_id}'


@asynccontextmanager
async def room_lock(room_id: str):
    async with async_redis_client.lock(f'room-{room_id}'):
        yield


def create_room(room: _RoomType):
    set_room(room)


def delete_room(room_id: str):
    redis_client.json().delete(get_room_key(room_id), Path.root_path())


def get_room(room_id: str, model: type[_RoomType]) -> _RoomType:
    room_dict = redis_client.json().get(get_room_key(room_id), Path.root_path())
    return model.parse_obj(room_dict)


def set_room(room: _RoomType):
    redis_client.json().set(get_room_key(room.id), Path.root_path(), json.loads(room.json()))


@asynccontextmanager
async def modify_room(
        room_id: str,
        model: type[_RoomType] = BaseRoom,
        notify: bool = True
) -> AsyncContextManager[_RoomType]:
    assert model.get_mode() is not None  # Modifying abstract models will lead to unexpected results

    async with room_lock(room_id):
        room = get_room(room_id, model)
        try:
            yield room
        except Exception:
            raise
        else:
            set_room(room)

            if notify:
                await notify_room(room)
