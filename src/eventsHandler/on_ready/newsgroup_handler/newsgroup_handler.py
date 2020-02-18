from typing import *
from src.utils.newsgroup_manager import NewsGroupManager
from src.utils.embeds_manager import EmbedsManager
import discord
from datetime import datetime, timedelta
import asyncio
import nntplib


async def print_news(client: discord.Client, news_id: str, group:str, group_manager: NewsGroupManager) -> datetime:
    info = dict()
    _, head = group_manager.NNTP.head(news_id)
    last = "NULL"
    for l in head.lines:
        s = l.decode(group_manager.encoding).split(": ", 1)
        print(s)
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
    msg = [content[i:i+5120] for i in range(0, len(content), 5120)]
    # print msg in every channel newsgroup_filler_embed
    embed = EmbedsManager.newsgroup_embed(subject, tags, msg[0], author, date, group_manager.groups[group]["name"])
    for channel in group_manager.groups[group]["channels"]:
        await client.get_channel(channel).send(embed=embed)
    for m in msg:
        embed = EmbedsManager.newsgroup_filler_embed(m, author, date, group_manager.groups[group]["name"])
        for channel in group_manager.groups[group]["channels"]:
            await client.get_channel(channel).send(embed=embed)

    return date


async def get_news(client: discord.Client):
    group_manager = NewsGroupManager()
    group_manager.get_config()
    group_manager.init_connection()
    while True:
        for group in group_manager.groups:
            try:
                last_update: datetime = datetime.strptime(group_manager.groups[group]["last_update"],
                                                          "%d/%m/%Y %H:%M:%S")
                _, news = group_manager.NNTP.newnews(group_manager.groups[group]["name"], last_update)
                for i in news:
                    d: datetime = await print_news(client, i, group, group_manager)
                    if d > last_update:
                        last_update = d
                group_manager.groups[group]["last_update"] = (last_update + timedelta(seconds=42)).strftime(
                    "%d/%m/%Y %H:%M:%S")
                await asyncio.sleep(60)
            except:
                print("Unexpected error for group " + group_manager.groups[group]["name"])


