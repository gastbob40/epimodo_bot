import discord

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager

api_manager = APIManager()


class LogManager:

    @staticmethod
    async def complete_log(client: discord.Client, sanction_type: str, author: discord.Member or discord.User,
                           guild: discord.Guild, reason: str, image_url: str = ''):
        state, results = api_manager.get_data('servers', discord_id=guild.id)

        if not state:
            return

        log_channel_id = results[0]['discord_log_channel_id']
        log_channel: discord.TextChannel = client.get_channel(log_channel_id)
        embed = EmbedsManager.sanction_embed(sanction_type, guild, reason, image_url)
        embed.description = f"Sanction by {author.display_name}"

        if log_channel:
            await log_channel.send(
                embed=embed
            )

        main_channel_log = client.get_channel(553974648258166800)
        if main_channel_log:
            embed.set_thumbnail(url=guild.icon_url)
            await main_channel_log.send(
                embed=embed
            )

    @staticmethod
    async def error_log(client: discord.Client, error_content: str, guild: discord.Guild):
        state, results = api_manager.get_data('servers', discord_id=guild.id)

        if not state:
            return

        log_channel_id = results[0]['discord_log_channel_id']
        log_channel: discord.TextChannel = client.get_channel(log_channel_id)
        embed = EmbedsManager.error_embed(error_content)

        if log_channel:
            await log_channel.send(
                embed=embed
            )

        main_channel_log = client.get_channel(553974648258166800)
        if main_channel_log:
            embed.set_thumbnail(url=guild.icon_url)
            await main_channel_log.send(
                embed=embed
            )
