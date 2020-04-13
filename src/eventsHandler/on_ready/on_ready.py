import datetime

import discord
import yaml

from src.eventsHandler.on_ready.newsgroup_handler.newsgroup_handler import get_news


class OnReady:
    @staticmethod
    async def login_information(client: discord.Client):
        print('We have logged in as {0.user}'.format(client))

        with open('run/config/newsgroups.yml', 'r') as file:
            config = yaml.safe_load(file)

        # config['last_update'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        with open(r'run/config/newsgroups.yml', 'w') as file:
            documents = yaml.dump(config, file)

        await get_news(client)
