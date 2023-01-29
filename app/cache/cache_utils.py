import json

from fastapi.encoders import jsonable_encoder

from app.cache.redis import redis


async def get_cache(prefix, id):
    key = generate_key(prefix, id)
    value = await redis.get(key)
    return json.loads(value) if value else None


async def set_cache(prefix, id, value):
    key = generate_key(prefix, id)
    await redis.set(key, json.dumps(jsonable_encoder(value)))


async def clear_cache(prefix, id):
    key = generate_key(prefix, id)
    keys = await redis.keys(f'{key}*')
    if keys:
        await redis.delete(*keys)


def generate_key(prefix, id):
    key = f'{prefix}:{id}'
    return key
