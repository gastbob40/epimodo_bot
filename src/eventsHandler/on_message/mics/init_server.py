from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def init_server(client: discord.Client, message: discord.Message, args: List[str]):
    state, results = permissions_manager.get_permissions(message.author, message.guild)

    if not state:
        await message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    if results != 3:
        await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )
        return

    state, results = api_manager.get_data('servers', discord_id=message.guild.id)
    if not state:
        await message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )
        return

    elif len(results) != 0:
        await message.channel.send(
            embed=EmbedsManager.error_embed('This server is already initialized.')
        )
        return

    state, results = api_manager.post_data('servers',
                                           discord_id=message.guild.id,
                                           discord_name=message.guild.name,
                                           discord_icon=message.guild.icon_url._url,
                                           discord_admin_role_id=1,
                                           discord_modo_role_id=1
                                           )

    if not state:
        await message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    await message.channel.send(
        embed=EmbedsManager.complete_embed(f"The `{message.guild.name}` server has been successfully added.\n"
                                           f"Please modify the ids of the admin and modo roles directly on the site.")
    )
