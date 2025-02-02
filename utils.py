import json
import asyncio
import aiofiles

json_filepath = "./games.json"
json_lock = asyncio.Lock()


async def get_games():
    async with json_lock:
        async with aiofiles.open(json_filepath, "r") as file:
            file_data = await file.read()
            games = json.loads(file_data)
            return games


def gamedata_to_json():
    pass
