from ._core import mongodb

collection = mongodb.logdb

# pmlogs


async def is_pmlogs(on_off: int) -> bool:
    onoff = await collection.find_one({"on_off": on_off})
    if not onoff:
        return False
    return True


async def add_on(on_off: int):
    is_on = await is_pmlogs(on_off)
    if is_on:
        return
    return await collection.insert_one({"on_off": on_off})


async def add_off(on_off: int):
    is_off = await is_pmlogs(on_off)
    if not is_off:
        return
    return await collection.delete_one({"on_off": on_off})


async def is_gruplogs(on_off: int) -> bool:
    onoff = await collection.find_one({"on_off": on_off})
    if not onoff:
        return False
    return True


async def addg_on(on_off: int):
    is_on = await is_gruplogs(on_off)
    if is_on:
        return
    return await collection.insert_one({"on_off": on_off})


async def addg_off(on_off: int):
    is_off = await is_gruplogs(on_off)
    if not is_off:
        return
    return await collection.delete_one({"on_off": on_off})
