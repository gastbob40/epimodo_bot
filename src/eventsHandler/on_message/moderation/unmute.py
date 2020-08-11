from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.log_manager import LogManager
from src.utils.permissions_manager import PermissionsManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def unmute(client: discord.Client, message: discord.Message, args: List[str]):
    state, results = permissions_manager.get_permissions(message.author, message.guild)

    if not state:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    # Check lvl permissions
    if results == 0:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )

    # Display help
    if args and args[0] == '-h':
        return await message.channel.send(
            embed=EmbedsManager.information_embed("**UnMuting command reminder:**\n\n"
                                                  "`!unmute <@user> (<#channel>)`.\n")
        )

    # Check if target exist
    target: discord.Member = message.mentions[0] if len(message.mentions) == 1 else False

    if not target:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Error in the command. You must mention an user.")
        )

    # Check role
    _, target_results = permissions_manager.get_permissions(target, message.guild)

    if target_results >= results:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("You cannot unmute someone greater than or equal to you.")
        )

    channels = message.channel_mentions if len(message.channel_mentions) >= 1 else [message.channel]
    await message.channel.send(
        embed=EmbedsManager.complete_embed(f"You just unmuted {target.display_name} in channel(s) : "
                                           f"{' '.join([chan.name for chan in channels]) }.")
    )

    await LogManager.complete_log(client, 'unmutes', message.author, message.guild,
                                          f"unmuted {target.display_name} in channel(s) : "
                                          f"{' '.join([chan.name for chan in channels]) }.", '')

    for channel in channels:
        try:
            if not target.permissions_in(channel).send_messages:
                await channel.set_permissions(target,
                                              overwrite=None)
        except:
            pass
