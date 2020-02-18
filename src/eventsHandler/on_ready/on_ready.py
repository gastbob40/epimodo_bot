import discord
from src.eventsHandler.on_ready.newsgroup_handler.newsgroup_handler import get_news


class OnReady:
    @staticmethod
    async def login_information(client: discord.Client):
        print('We have logged in as {0.user}'.format(client))
        await get_news(client)
