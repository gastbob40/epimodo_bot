import asyncio
from typing import List

import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def clear_messages(client: discord.Client, message: discord.Message, args: List[str]):
    channel: discord.TextChannel = message.channel
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
            embed=EmbedsManager.information_embed("**Clearing command reminder:**\n\n"
                                                  "`!clear <number of message>`.")
        )

    # Check argument validity
    if not args:
        return await message.channel.send(
            embed=EmbedsManager.error_embed("Error in the command. You must add a number of message (limit to 100).")
        )

    if not args[0].isdigit():
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Error in the command. You must specify a valid number of message (limit to 100).")
        )

    message_count = int(args[0])

    if message_count <= 0 or message_count > 100:
        return await message.channel.send(
            embed=EmbedsManager.error_embed(
                "Error in the command. You must specify a number of message between  1 and 100.")
        )

    # Send message
    sent_message: discord.Message = await message.channel.send(
        embed=EmbedsManager.complete_embed(f"Do you really want to delete {message_count} messages ?\n"
                                           f"*You have 20s to accept.*")
    )

    # Add reaction
    await sent_message.add_reaction('🆗')

    # Check response
    def check(reaction, user):
        return user == message.author and (str(reaction.emoji) == '🆗')

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
    except asyncio.TimeoutError:
        await message.channel.send(f"You have canceled the clear.")
    else:
        # check response
        async for m in channel.history(limit=message_count):
            await m.delete()

        await message.channel.send(f"The deletion of the messages was successfully completed")
