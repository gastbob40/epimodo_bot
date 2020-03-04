import asyncio
import nntplib
from datetime import datetime, timedelta

import discord
import yaml

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.newsgroup_manager import NewsGroupManager

api_manager = APIManager()


async def print_news(client: discord.Client, news_id: str, group: dict, group_manager: NewsGroupManager) -> datetime:
    info = dict()
    _, head = group_manager.NNTP.head(news_id)
    last = "NULL"
    for l in head.lines:
        s = l.decode(group_manager.encoding).split(": ", 1)
        if len(s) != 2:
            info[last] = info[last] + nntplib.decode_header(s[0])
            continue
        last = s[0]
        info[s[0]] = nntplib.decode_header(s[1])
    author = info["From"]
    subject = info["Subject"]
    d = info["Date"][:25]
    if d[-1] == " ":
        d = d[:-1]
    date = datetime.strptime(d, "%a, %d %b %Y %H:%M:%S")

    _, body = group_manager.NNTP.body(news_id)
    content = ""
    for l in body.lines:
        content += l.decode(group_manager.encoding) + "\n"

    # get the tags
    tags = []
    s = subject.split("]", 1)
    while len(s) != 1:
        tags.append((s[0])[1:])
        s = s[1].split("]", 1)
    subject = s[0]
    # slice the msg in chunk of 5120 char
    msg = [content[i:i + 5120] for i in range(0, len(content), 5120)]

    # print msg in every channel newsgroup_filler_embed
    embed = EmbedsManager.newsgroup_embed(subject, tags, msg[0], author, date, group["name"])

    for guild in group['channels']:
        print(" - " + client.get_channel(int(guild['channel_id'])).name)
        await client.get_channel(int(guild['channel_id'])).send(embed=embed)

    for i in range(1, len(msg)):
        embed = EmbedsManager.newsgroup_filler_embed(msg[i], author, date, group["name"])
        for guild in group['channels']:
            await client.get_channel(int(guild['channel_id'])).send(embed=embed)

    return date


async def get_news(client: discord.Client):
    group_manager = NewsGroupManager()
    group_manager.get_config()

    with open('run/config/newsgroups.yml', 'r') as file:
        config = yaml.safe_load(file)

    while True:
        try:

            # Load data from API
            state, res = api_manager.get_data('news-groups')

            # Check if we get a response from the API
            if not state:
                return

            # Start the connection
            group_manager.open_connection()

            # For each news group, do magic
            for group in res:
                try:
                    print(group['name'])
                    # Get last update from config
                    last_update: datetime = datetime.strptime(config["last_update"], "%d/%m/%Y %H:%M:%S")
                    _, news = group_manager.NNTP.newnews(group['slug'], last_update)
                    for i in news:
                        try:
                            await print_news(client, i, group, group_manager)
                        except Exception as exe:
                            print("Unexpected error for news " + i)
                            print(exe)
                        config["last_update"] = (last_update +
                                                 timedelta(seconds=(0 if len(news) == 0 else 42))) \
                            .strftime("%d/%m/%Y %H:%M:%S")
                except Exception as exe:
                    print("Unexpected error for group " + group['name'])
                    print(exe)
            group_manager.close_connection()

            config["last_update"] = (datetime.now() +
                                     timedelta(seconds=42).strftime("%d/%m/%Y %H:%M:%S"))

            await asyncio.sleep(int(group_manager.delta_time))
        except Exception as exe:
            print("Error while updating")
        print(exe)
