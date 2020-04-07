import discord
from src.utils.log_manager import LogManager
from src.utils.embeds_manager import EmbedsManager


class OnMemberJoin:

    msg_fr: str = """Bienvenue sur le serveur {}.\n\n:red_circle: Pour avoir accès au serveur, vous devez \
    prouver que vous êtes un étudiant de l'école. Pour cela, merci de vous manifester dans le channel #contacts_staff. \
    Un modérateur s'occupera de vous valider et de vous donner les bons rôles.\n\n:grey_question: Vous pouvez \
    mentionner @Modo si le staff ne remarque pas votre arrivée."""

    msg_eng: str = """Welcome to the {} server.\n\n:red_circle: To get access to the server, you need \
    to prove that you are a student of the school. For this, please send a message in the #contacts_staff channel.\
     A moderator will take care of validating your status and giving you the correct roles.\n\n:grey_question: You \
     can mention @Modo if the staff does not notice your arrival."""

    @staticmethod
    async def run(client: discord.client, user: discord.member):
        guild: discord.guild = user.guild
        pass # TODO TO FIX
        return
        embed = EmbedsManager.welcome_msg_embed(OnMemberJoin.msg_fr.format(guild.name),
                                                OnMemberJoin.msg_eng.format(guild.name))
        try:
            await user.send(embed=embed)
        except discord.Forbidden:
            await LogManager.error_log(client, "OnMemberJoin: Unable to send msg to " + user.nick + " -> Forbidden",
                                       guild)
        except discord.HTTPException:
            await LogManager.error_log(client, "OnMemberJoin: Unable to send msg to " + user.nick + " -> HTTPException",
                                       guild)
        except discord.InvalidArgument:
            await LogManager.error_log(client, "OnMemberJoin: Unable to send msg to " + user.nick +
                                       " -> InvalidArgument", guild)
        except:
            await LogManager.error_log(client, "OnMemberJoin: Unable to send msg to " + user.nick + " -> Unknown",
                                       guild)
