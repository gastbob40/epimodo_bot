from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager
from src.utils.log_manager import LogManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def unban(client: discord.Client, message: discord.Message, args: List[str]):
    state, results = permissions_manager.get_permissions(message.author, message.guild)

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    # Check lvl permissions
    if results == 0 or results == 1:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**Unbanning command reminder:**\n\n"
                                                  "`!unban <@user>`.")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Error in the command. You must mention an user.")
        )

    await message.channel.send(
        embed=EmbedsManager.complete_embed(f"You just unbanned {target.display_name}.")
    )

    await LogManager.complete_log(client, 'bans', message.author, message.guild, "", "")

    try:
        await target.send(
            embed=EmbedsManager.information_embed("You have been unbanned"
                                                  " from the server {}".format(message.guild.name))
        )
        await target.unban(reason="")
    except:
        await message.channel.send(
            embed=EmbedsManager.error_embed("Error in banning the member.")
        )
