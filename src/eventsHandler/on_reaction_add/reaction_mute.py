import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager
from src.utils.log_manager import LogManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def mute(client: discord.Client, reaction: discord.Reaction, user: discord.User):
    state, results = permissions_manager.get_permissions(user, reaction.message.guild)

    if not state:
        return await reaction.message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    # Check lvl permissions
    if results == 0:
        return

    target: discord.Member = reaction.message.author

    # Check role
    _, target_results = permissions_manager.get_permissions(target, reaction.message.guild)

    if target_results >= results:
        return

    try:
        if target.permissions_in(reaction.message.channel).read_messages:
            await reaction.message.channel.set_permissions(target,
                                          send_messages=False)
        else:
            return
    except:
        await reaction.message.channel.send(
            embed=EmbedsManager.error_embed("Error in muting the member.")
        )

    await reaction.message.channel.send(
        embed=EmbedsManager.complete_embed(f"You just muted {target.display_name} in channel : "
                                           f"{reaction.message.channel.name}.")
    )

    await LogManager.complete_log(client, 'mutes', reaction.message.author, reaction.message.guild,
                                          f"muted {target.display_name} in channel(s) : "
                                           f"{reaction.message.channel.name}.", '')
