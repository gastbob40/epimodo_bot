from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def get_user(client: discord.Client, message: discord.Message, args: List[str]):
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
            embed=EmbedsManager.information_embed("**Server command reminder:** \n\n"
                                                  "`!user`.\n"
                                                  "You can optionally add a mention to a user to get it profile")
        )

    if not message.mentions:
        await message.channel.send(
            embed=EmbedsManager.complete_embed(f"https://epimodo.gastbob40.ovh/moderation/profile/")
        )
    else:
        await message.channel.send(
            embed=EmbedsManager.complete_embed(
                f"https://epimodo.gastbob40.ovh/moderation/profile/{message.mentions[0].id}")
        )
