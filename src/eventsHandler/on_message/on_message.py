import discord
import yaml

from src.eventsHandler.on_message.mics.check_mentions import check_mentions
from src.eventsHandler.on_message.mics.get_server import get_server
from src.eventsHandler.on_message.mics.get_user import get_user
from src.eventsHandler.on_message.mics.init_server import init_server
from src.eventsHandler.on_message.mics.reload_bot import reload_bot
from src.eventsHandler.on_message.moderation.add_ban import add_ban
from src.eventsHandler.on_message.moderation.unban import unban
from src.eventsHandler.on_message.moderation.add_kick import add_kick
from src.eventsHandler.on_message.moderation.add_general_mute import add_general_mute
from src.eventsHandler.on_message.moderation.mute import mute
from src.eventsHandler.on_message.moderation.add_warn import add_warn
from src.eventsHandler.on_message.moderation.clear_messages import clear_messages
from src.eventsHandler.on_message.moderation.remove_general_mute import remove_general_mute
from src.eventsHandler.on_message.moderation.unmute import unmute
from src.eventsHandler.on_message.moderation.get_mutes import get_mutes


class OnMessage:
    @staticmethod
    async def run(client: discord.Client, message: discord.Message):
        if message.author.bot:
            return

        with open('run/config/config.yml', 'r') as file:
            config = yaml.safe_load(file)

        await check_mentions(client, message)

        if message.content and message.content[0] != config['prefix']:
            return

        command = message.content.split(' ')[0][1:]
        args = message.content.split(' ')[1:]

        if command == 'init':
            await init_server(client, message, args)
        if command == 'reload':
            await reload_bot(client, message, args)

        # Sanctions manager
        elif command == 'warn':
            await add_warn(client, message, args)
        elif command == 'kick':
            await add_kick(client, message, args)
        elif command == 'ban':
            await add_ban(client, message, args)
        elif command == 'unban':
            await unban(client, message, args)
        elif command == 'g_mute':
            await add_general_mute(client, message, args)
        elif command == 'g_unmute':
            await remove_general_mute(client, message, args)
        elif command == 'mute':
            await mute(client, message, args)
        elif command == 'get_mutes':
            await get_mutes(client, message, args)
        elif command == 'unmute':
            await unmute(client, message, args)
        elif command == 'clear':
            await clear_messages(client, message, args)

        elif command == 'server':
            await get_server(client, message, args)
        elif command == 'user':
            await get_user(client, message, args)
