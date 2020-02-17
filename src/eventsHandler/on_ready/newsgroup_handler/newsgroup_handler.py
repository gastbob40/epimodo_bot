from typing import *
from src.utils.newsgroup_manager import NewsGroupManager
import nntplib
import discord
from datetime import datetime
import time


async def print_news(client: discord.Client, news_id: str, group_manager: NewsGroupManager) -> datetime:
    info = dict()
    head: nntplib.ArticleInfo = group_manager.NNTP.head(news_id)
    for l in head.lines:
        s = l.split(":")
        if len(s) != 2:
            continue
        info[s[0]] = s[1]
    author = info["From"]
    subject = info["Subject"]
    date = datetime.strptime(info["Date"], "%a, %d %b %Y %H:%M:%S %z")

    body: nntplib.ArticleInfo = group_manager.NNTP.body(news_id)
    content = ""
    for l in body.lines:
        content += l + "\n"

    # TODO : send to dicord

    return date


async def get_news(client: discord.Client, group_manager: NewsGroupManager):
    group_manager.get_config()
    group_manager.init_connection()
    while True:
        for group in group_manager.groups:
            last_update = datetime.strptime(group_manager.groups[group]["last_update"], "%d/%m/%Y %H:%M:%S")
            _, news = group_manager.NNTP.newnews(group_manager.groups[group]["name"], last_update)
            for i in news:
                d = await print_news(client, i, group_manager)
                if d > last_update:
                    last_update = d
            group_manager.groups[group]["last_update"] = last_update.strftime("%d/%m/%Y %H:%M:%S")
            time.sleep(60) # TODO change to async maybe


