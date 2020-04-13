from typing import List
import discord
import git
import subprocess

from src.utils.api_manager import APIManager
from src.utils.embeds_manager import EmbedsManager
from src.utils.permissions_manager import PermissionsManager

api_manager = APIManager()
permissions_manager = PermissionsManager()


async def reload_bot(client: discord.Client, message: discord.Message, args: List[str]):
    if message.author.id != 309653542354944000:
        return

    try:
        repo = git.Repo()
        current = repo.head.commit
        repo.remotes.origin.pull()
        if current != repo.head.commit:
            await message.channel.send(
                embed=EmbedsManager.complete_embed(
                    f"I just pulled\n - `{repo.head.commit.summary}` by `{repo.head.commit.author}`.")
            )

            subprocess.run(["pm2", "restart", "19"])
        else:
            await message.channel.send(
                embed=EmbedsManager.error_embed("Noting to pull")
            )
    except:
        await message.channel.send(
            embed=EmbedsManager.error_embed("Error on pulling")
        )
