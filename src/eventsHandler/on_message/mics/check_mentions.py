import discord
import yaml

from src.utils.api_manager import APIManager

api_manager = APIManager()


async def check_mentions(client: discord.Client, message: discord.Message):
    if len(message.mentions) < 4 and len(message.role_mentions) == 0 and not message.mention_everyone:
        return

    embed = discord.Embed()
    embed.set_thumbnail(url=message.author.avatar_url) \
        .set_author(name="A message with important notification has been sent.",
                    icon_url="https://cdn4.iconfinder.com/data/icons/infy-interface/300/notification-512.png")
    embed.add_field(name=f'Message by {message.author.display_name}',
                    value=message.clean_content.content[:1200])

    state, results = api_manager.get_data('servers', discord_id=message.guild.id)

    if not state:
        return

    log_channel_id = results[0]['discord_log_channel_id']
    log_channel: discord.TextChannel = client.get_channel(log_channel_id)

    with open('run/config/config.yml', 'r') as file:
        config = yaml.safe_load(file)

    main_channel_log = client.get_channel(config['channels']['log_channel'])

    if log_channel:
        await log_channel.send(
            embed=embed
        )

    if main_channel_log:
        embed.set_thumbnail(url=message.guild.icon_url)
        await main_channel_log.send(
            embed=embed
        )
