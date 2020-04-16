import discord
import yaml

from src.eventsHandler.eventsHandler import EventsHandler
from src.utils.embeds_manager import EmbedsManager
# Get configuration
from src.utils.permissions_manager import PermissionsManager
from src.utils.api_manager import APIManager

sanctions_manager = APIManager()
permissions_manager = PermissionsManager()

with open('run/config/tokens.yml', 'r') as file:
    tokens = yaml.safe_load(file)

client = discord.Client()

@client.event
async def on_message(message: discord.Message):
    await EventsHandler.on_message(client, message)


@client.event
async def on_reaction_add(reaction, user):
    await EventsHandler.on_reaction_add(client, reaction, user)


@client.event
async def on_member_join(member):
    await EventsHandler.on_member_join(client, member)


client.run(tokens['discord_token'])
