import discord
import json
import asyncio
import aiohttp
import aiofiles

json_filepath = "./games.json"
json_lock = asyncio.Lock()

""" helper functions"""


async def get_saved_games():
    async with json_lock:
        async with aiofiles.open(json_filepath, "r") as file:
            file_data = await file.read()
            games = json.loads(file_data)
            return games


async def search_game(game):
    """makes a request for the search results from IFDB, and returns the object containing the list of games"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://ifdb.org/search?json&game&searchfor={game}"
        ) as res:
            print(res.status)
            games = await res.json()
            return games


def gamedata_to_json():
    pass


def format_search_result(search_results: dict) -> list:
    """takes the list of games returned from the search and converts them into pages of embeds."""
    if len(search_results) == 0:
        return [discord.Embed(description="no results")]
    pages = []
    for game in search_results["games"]:
        pages.append(discord.Embed(description=game))
    return pages


class PageView(discord.ui.View):
    def __init__(self, interaction, pages):
        super().__init__(timeout=60)
        self.interaction_user = interaction.user
        self.pages = pages
        self.current_page = 0
        self.buttonModal.label = f"{self.current_page+1}/{len(self.pages)}"

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.interaction.user:
            return True
        else:
            emb = discord.Embed(
                description=f"Only the author of the command can perform this action.",
                color=16711680,
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)
            return False
