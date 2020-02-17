from datetime import datetime, timedelta
import discord
from random import randint


class EmbedsManager:

    @staticmethod
    def complete_embed(content):
        embed = discord.Embed(color=0x19D773)\
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/shift-free/32/Complete_Symbol-512.png",
                        name="The command was successful.")
        embed.timestamp = datetime.now() - timedelta(hours=2)
        embed.description = content
        return embed

    @staticmethod
    def information_embed(content):
        embed = discord.Embed(color=0xEFCC00) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/simply-orange-1/128/questionssvg-512.png",
                        name="Additional information.")
        embed.timestamp = datetime.now() - timedelta(hours=2)
        embed.description = content
        return embed

    @staticmethod
    def error_embed(content):
        embed = discord.Embed(color=0xD72727) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/shift-free/32/Error-512.png",
                        name="An error has occurred.")
        embed.timestamp = datetime.now() - timedelta(hours=2)
        embed.description = content
        return embed

    @staticmethod
    def sanction_embed(sanction_type: str, guild: discord.Guild, reason, image_url=''):
        embed = discord.Embed(color=0x0000) \
            .set_author(icon_url="https://cdn0.iconfinder.com/data/icons/tools-icons-rounded/110/Hammer-512.png",
                        name=f"New sanction from {guild.name}") \
            .add_field(name=f'Sanction type: {sanction_type.capitalize()}',
                       value=f'Reason: {reason}')

        if image_url:
            embed.set_image(image_url)

        embed.timestamp = datetime.now() - timedelta(hours=2)

        return embed

    colors = ["css\n", "http\n", "cs\n# ", "yaml\n", "md\n# ", ""]

    @staticmethod
    def newsgroup_embed(title, tags, msg, author, date: datetime, group):
        embed = discord.Embed(color=0x0080ff, title=title)
        color = randint(0, 4)
        for tag in tags:
            embed.add_field(name="​", value="```{}{}```".format(EmbedsManager.colors[color], tag), inline=True)
            color = randint(0, 4)
        parts = [msg[i:i+1024] for i in range(0, len(msg), 1024)]
        embed.add_field(name="{}\n{}".format(author, date.strftime("%a, %d %b %Y %H:%M")), value=parts[0], inline=False)
        for i in range(1, len(parts)):
            embed.add_field(name="​", value=parts[i], inline=False)
        embed.set_footer(text=group)
        return embed

    @staticmethod
    def newsgroup_filler_embed(msg, author, date: datetime, group):
        embed = discord.Embed(color=0x0080ff)
        parts = [msg[i:i+1024] for i in range(0, len(msg), 1024)]
        embed.add_field(name="{}\n{}".format(author, date.strftime("%a, %d %b %Y %H:%M")), value=parts[0], inline=False)
        for i in range(1, len(parts)):
            embed.add_field(name="​", value=parts[i], inline=False)
        embed.set_footer(text=group)
        return embed



