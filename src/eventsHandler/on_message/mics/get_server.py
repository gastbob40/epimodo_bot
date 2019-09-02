from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def get_server(client: discord.Client, message: discord.Message, args: List[str]):
    state, results = permissions_manager.get_permissions(message.author, message.guild)

    if not state:
        await message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    if results == 0:
        await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )
        return

    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Server command reminder:**\n\n"
                                                  "`!server`.")
        )

    await message.channel.send(
        embed=EmbedsManager.complete_embed(f"https://epimodo.gastbob40.ovh/moderation/servers/{message.guild.id}")
    )
