import random
from datetime import datetime

import discord
from Class import Hashmap, Binary_tree
from discord.ext import commands

intents = discord.Intents.all()
NightFuryAssistant = commands.Bot(command_prefix="!", intents=intents)
binary_tree = Binary_tree()
class CustomHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        help_message = (
            "Voici quelques-unes des commandes disponibles :\n"
            "`!last` - Affiche la dernière commande utilisée.\n"
            "`!history` - Affiche l'historique des commandes de l'utilisateur.\n"
            "`!clear_history` - Vide l'historique des commandes de l'utilisateur.\n"
            "`!dance` - ça danse !!\n"
            "`!ban` - Bannit un utilisateur du serveur.\n"
            "`!kick` - Expulse un utilisateur du serveur.\n"
            "`!shutdown` - Arrête le bot.\n"
            "\n Attention il y a aussi des mots clé qui renvoie a des gif secret a vous de les trouver ^^ \n\n "
            
            "Pour plus d'informations sur une commande spécifique, utilisez `!help [nom de la commande]`."
        )
        await self.get_destination().send(help_message)

NightFuryAssistant.help_command = CustomHelpCommand()





command_history = Hashmap(size=10000)
command_history.load_from_file("command_history.json")


@NightFuryAssistant.command(name='last', help='Affiche la dernière commande utilisée')
async def last_command(ctx):
    user_id = ctx.author.id
    user_history = command_history.get(user_id)

    if user_history and len(user_history) > 0:
        last_command = user_history[-1]
        await ctx.send(f'Dernière commande: {last_command}')
    else:
        await ctx.send('Aucune commande dans l\'historique pour cet utilisateur.')

@NightFuryAssistant.command(name='history', help='Affiche l\'historique')
async def user_history(ctx):
    user_id = ctx.author.id
    user_history = command_history.get(user_id)

    if user_history and len(user_history) > 0:
        user_commands = '\n'.join(user_history)
        await ctx.send(f'Historique des commandes pour cet utilisateur:\n{user_commands}')
    else:
        await ctx.send('Aucune commande dans l\'historique pour cet utilisateur.')

@NightFuryAssistant.command(name='clear_history', help='Supprime l\'historique')
async def clear_history(ctx):
    user_id = ctx.author.id
    user_history = command_history.get(user_id)

    if user_history and len(user_history) > 0:
        previous_history = user_history.copy()
        user_history.clear()
        await ctx.send(f'Historique vidé pour cet utilisateur. Anciennes commandes:\n{", ".join(previous_history)}')
    else:
        await ctx.send('Aucune commande dans l\'historique pour cet utilisateur.')


@NightFuryAssistant.command(name='dance', help='ça dance !!')
async def dance(ctx):
    dance_gif_urls = [
        "https://tenor.com/view/toothless-toothless-dragon-lizard-dance-dancing-gif-18147614732076936345",
        "https://tenor.com/view/light-fury-dancing-gif-9809758880728697278",
        "https://tenor.com/view/nightfury-lightfury-howtotraindragon-howtotraindragon3-toothless-gif-2440374806486612673",
    ]
    random_gif_url = random.choice(dance_gif_urls)
    await ctx.send(random_gif_url)

@NightFuryAssistant.command(name='shutdown', help='Arrête le bot')
async def shutdown(ctx):
    await ctx.send("Arrêt du bot...")
    command_history.save_to_file("command_history.json")
    print("Données sauvegardées avant l'arrêt du bot.")
    await NightFuryAssistant.close()

@NightFuryAssistant.command(name='ban', help='Bannit un utilisateur du serveur.')
@commands.has_permissions(ban_members=True)
async def ban_user(ctx, user: discord.Member, *, reason=None):
    try:
        await user.ban(reason=reason)
        await ctx.send(f"{user.mention} a été banni du serveur. Raison: {reason}")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas les autorisations nécessaires pour bannir cet utilisateur.")
    except discord.HTTPException:
        await ctx.send("Une erreur s'est produite lors de la tentative de bannissement de cet utilisateur.")

@NightFuryAssistant.command(name='kick', help='Expulse un utilisateur du serveur.')
@commands.has_permissions(kick_members=True)
async def kick_user(ctx, user: discord.Member, *, reason=None):
    try:
        await user.kick(reason=reason)
        await ctx.send(f"{user.mention} a été expulsé du serveur. Raison: {reason}")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas les autorisations nécessaires pour expulser cet utilisateur.")
    except discord.HTTPException:
        await ctx.send("Une erreur s'est produite lors de la tentative d'expulsion de cet utilisateur.")



@NightFuryAssistant.event
async def on_message(message):
    if message.author == NightFuryAssistant.user:
        return

    if message.content.lower() in ["oui", "non"]:
        response = binary_tree.send_answer(message.content)
        await message.channel.send(response)

    await NightFuryAssistant.process_commands(message)

@NightFuryAssistant.event
async def on_command(ctx):
    user_id = ctx.author.id
    command = ctx.message.content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    user_history = command_history.get(user_id)
    if user_history is None:
        user_history = []
        command_history.set_key_value(user_id, user_history)

    user_history.append(command +"      |  "+ timestamp)
    command_history.save_to_file("command_history.json")

    max_history_size = 10
    if len(user_history) > max_history_size:
        user_history = user_history[-max_history_size:]

@NightFuryAssistant.event
async def on_ready():
    print("NightFury Assistant est prêt !")

@NightFuryAssistant.event
async def on_typing(channel, user, when):
    await channel.send("Attention " + user.name + " je te regarde")

@NightFuryAssistant.event
async def on_member_join(member):
    general_channel = NightFuryAssistant.get_channel(1059759796594675755)
    url = "https://tenor.com/view/toothless-gif-9515653027378292131"
    await general_channel.send("Bienvenue sur le serveur ! " + member.name)
    await general_channel.send(url)

@NightFuryAssistant.event
async def on_message(message):
    if message.author == NightFuryAssistant.user:
        return
    message.content = message.content.lower()

    if message.content.startswith("hello"):
        url = "https://cdn.discordapp.com/attachments/1059759796594675755/1194042357373476985/TheUltimateHowToTrainYourDragonRecapCartoon-ezgif.com-video-to-gif-converter_1.gif?ex=65aee99a&is=659c749a&hm=f5e8e97b92ced20b90efc1ce66bebf7408f43fb4758bbd268f3705812ab37f4d&"
        await message.channel.send(url)
        await message.channel.send("*Slurp*")

    if "sniper" in message.content:
        url = "https://cdn.discordapp.com/attachments/1059759796594675755/1194042357851639839/TheUltimateHowToTrainYourDragonRecapCartoon-ezgif.com-video-to-gif-converter.gif?ex=65aee99a&is=659c749a&hm=efeaa9e8d62fd243e4b66692ae65f893c15addd102aa5d33115d03181d3630e2&"
        await message.channel.send(url)
        await message.channel.send("RRRRRRRRRRrrRRrRRrrrrrRrrrrrr.......")

    if "faim" in message.content:
        url = "https://cdn.discordapp.com/attachments/1059759796594675755/1194042356916310097/TheUltimateHowToTrainYourDragonRecapCartoon-ezgif.com-video-to-gif-converter_2.gif?ex=65aee99a&is=659c749a&hm=2d15047999fe27da39fad50d31b33bcd802e1af536162f0902ca7b4c6d0aee1e&"
        await message.channel.send(url)
        await message.channel.send("Yum Yum Yum Yum Yum Yum yum")

    await NightFuryAssistant.process_commands(message)




NightFuryAssistant.run("MTE2NzM5NzAxNzg5NTU3MTQ3Nw.GQKZcD.BMBRCaW8vyEo4qC4nQZS_-PrTH6xND-KnJOwE8")
