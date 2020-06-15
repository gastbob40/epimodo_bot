import discord

from src.eventsHandler.on_reaction_add.report_message import report_message
from src.eventsHandler.on_reaction_add.reaction_mute import mute
from src.eventsHandler.on_reaction_add.reaction_unmute import unmute


class OnReactionAdd:
    @staticmethod
    async def run(client: discord.Client, reaction: discord.Reaction, user: discord.User):

        if user.bot:
            return

        if reaction.emoji in ["⚠️", "⚠"]:
            await report_message(client, reaction, user)

        if reaction.emoji == "🔇":
            await mute(client, reaction, user)
        if reaction.emoji in ["🔉", "🔊"]:
            await unmute(client, reaction, user)
