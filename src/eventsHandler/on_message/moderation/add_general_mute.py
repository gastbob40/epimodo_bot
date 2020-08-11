from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager
from src.utils.log_manager import LogManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def add_general_mute(client: discord.Client, message: discord.Message, args: List[str]):
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
            embed=EmbedsManager.information_embed("**General Muting command reminder:**\n\n"
                                                  "`!g_mute <@user> <reason>`.\n"
                                                  "An image can be added to the command (it will be saved for logs).")
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
            embed=EmbedsManager.error_embed("You cannot mute someone greater than or equal to you.")
        )

    args = args[1:]

    if len(args) == 0:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Error in the command. You must add a reason.")
        )

    reason = ' '.join(args)

    image_url = message.attachments[0].proxy_url if len(message.attachments) == 1 else ''

    api_manager.post_data('mutes',
                          target_id=target.id,
                          author_id=message.author.id,
                          server_id=message.guild.id,
                          reason=reason,
                          is_active=True,
                          image=image_url)

    await message.channel.send(
        embed=EmbedsManager.complete_embed(f"You just muted {target.display_name} for {reason}.")
    )

    await LogManager.complete_log(client, 'general mutes', message.author, message.guild, reason, image_url)

    await target.send(
        embed=EmbedsManager.sanction_embed('Mute', message.guild, reason, image_url)
    )

    for channel in message.guild.channels:
        try:
            if target.permissions_in(channel).read_messages:
                await channel.set_permissions(target,
                                              send_messages=False)
        except:
            pass
