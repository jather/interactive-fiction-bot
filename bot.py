import discord
from discord.ext import commands
from dotenv import load_dotenv
import utils
import glk
import os
import asyncio
import aiohttp

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="!")
sessions = {}


# on view command: make api call using TUI from json to view details, has play button
# download command: if owner: input TUI and custom name. download into ./stories, and write into games.json
#
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.CustomActivity(name="being worked on by jather rn")
    )
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except discord.DiscordException as e:
        print("error syncing commands")
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id in sessions:
        channel_id = message.channel.id
        sessions[channel_id].send(message.content)
        await bot.get_channel(channel_id).send(sessions[channel_id].get_response())
    print(f"Received message: {message.content}")


@bot.tree.command(
    name="start", description="create a game session in the current channel"
)
async def start(interaction: discord.Interaction, game: str):
    channel_id = interaction.channel_id
    if channel_id in sessions:
        await interaction.response.send_message(
            "Session already exists in current channel"
        )
    else:
        # find file path from json file. if doesn't exist, send error message
        games = await utils.get_saved_games()
        if game.lower() not in games:
            await interaction.response.send_message("no game with that title in list")
            return
        game_path = games[game.lower()]["path"]
        sessions[channel_id] = glk.GLKSession(game_path)
        await interaction.response.send_message(
            f"Creating session. Channel id: {channel_id}",
        )
        await bot.get_channel(channel_id).send(sessions[channel_id].get_response())


@bot.tree.command(name="stop", description="terminate a session")
async def stop(interaction: discord.Interaction):
    channel_id = interaction.channel_id
    if channel_id not in sessions:
        await interaction.response.send_message("No session in current channel")
    else:
        await interaction.response.send_message("Terminating session")
        sessions[channel_id].end_session()
        del sessions[channel_id]


@bot.tree.command(name="list", description="list available games")
async def list_games(interaction: discord.Interaction):
    games = await utils.get_saved_games()
    await interaction.response.send_message([game for game in games])


@bot.tree.command(
    name="search", description="search for a title on IFDB and show the first result"
)
async def search(interaction: discord.Interaction, message: str):
    search_result = await utils.search_game(message)
    pages = utils.format_search_result(search_result)
    view = utils.PageView(discord.Interaction, pages)
    await interaction.response.send_message(embed=pages[0], view=view)


@bot.tree.command(name="add", description="add a new game by downloading its file")
@commands.is_owner()
async def add(interaction: discord.Interaction, game: str):
    games = await utils.get_saved_games()
    if game.lower() in games:
        await interaction.response.send_message("we already have that game!")


bot.run(TOKEN)
