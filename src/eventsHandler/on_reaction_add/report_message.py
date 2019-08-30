import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager
from src.utils.log_manager import LogManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def report_message(client: discord.Client, reaction: discord.Reaction, user: discord.User):
    guild = reaction.message.guild

    await reaction.remove(user)

    state, results = permissions_manager.get_permissions(user, guild)

    if not state:
        return await reaction.message.channel.send(
            embed=EmbedsManager.error_embed(results)
        )

    # Check lvl permissions
    if results == 0:
        return await reaction.message.channel.send(
            embed=EmbedsManager.error_embed("You don't have the necessary permissions.")
        )

    # Check role
    _, target_results = permissions_manager.get_permissions(reaction.message.author, guild)

    if target_results >= results:
        return await reaction.message.channel.send(
            embed=EmbedsManager.error_embed("You cannot warn someone greater than or equal to you.")
        )

    reason = reaction.message.content

    api_manager.post_data('warns',
                          target_id=reaction.message.author.id,
                          author_id=user.id,
                          server_id=guild.id,
                          reason='Reported Message: ' + reason,
                          )

    await LogManager.complete_log(client, 'warns', user, guild, reason)

    try:
        await reaction.message.author.send(
            embed=EmbedsManager.sanction_embed('Reported Message', guild, reason)
        )
    except Exception as e:
        print(e)

