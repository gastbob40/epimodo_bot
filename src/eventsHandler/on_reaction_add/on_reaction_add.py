import discord

from src.eventsHandler.on_reaction_add.report_message import report_message


class OnReactionAdd:
    @staticmethod
    async def run(client: discord.Client, reaction: discord.Reaction, user: discord.User):

        if user.bot:
            return

        if reaction.emoji == "⚠":
            await report_message(client, reaction, user)
