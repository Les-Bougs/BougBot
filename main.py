import os
import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import random
import json

from Bougs import Boug
from load_save_bougs import save_bougs, load_bougs

load_dotenv(dotenv_path="config")

class BougBot(commands.Bot):
    def __init__(self):
        self.description = """Boug Bot, ton nouveau meilleur pote"""

        super().__init__(
            command_prefix=("!"),
            intents=discord.Intents.all(),
            escription=self.description,
            case_insensitive=True,
        )

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    async def on_ready(self):
        self.botid = f"<@{self.user.id}>"
        print(f"{self.user.display_name} est prêt.")
        self.list_members_guild = list(discord.utils.get(self.guilds, name="Les Bougs du fond").members)
        self.list_boug = []
        self.dict_boug = {}
        self.loaded_data = load_bougs(self)

        for guild_member in self.list_members_guild:
            # self.list_boug.append(self.list_members_guild[i].id, boug_bot.list_members_guild[i].name, 1000)
            if self.loaded_data.get(str(guild_member.id)):
                id_member = str(guild_member.id)
                self.dict_boug[guild_member.id] = Boug(
                    self.loaded_data[id_member]['id'],
                    self.loaded_data[id_member]['name'],
                    self.loaded_data[id_member]['money']
                    )
            else:
                self.dict_boug[guild_member.id] = Boug(guild_member.id, guild_member.name, 0)

    async def reply(self, message, list_words, response):
        if any(x in message.content.lower() for x in list_words):
            if self.botid in message.content:
                user = message.author
                await message.reply(f"{response} <@{user.id}>")

    async def on_message(self, message):
        await self.reply(message, ("merci","cimer","thanks","thx"), "De rien")
        await self.reply(message, ("salut","hello","wesh","bonjour"), "Salut")
        await self.reply(message, ("ntm","fdp","merde","putain","tg"), "Attention à ton langage ;-)")
        print(message.content)
        await self.process_commands(message)


def get_vocal_members(ctx, channel_name="Général"):
    return discord.utils.get(ctx.guild.channels, name=channel_name).members


boug_bot = BougBot()

# Custom bot commands below

# Display all members currently inside a given VoiceChannel
@boug_bot.command()
async def voclist(ctx):
    voc_members = get_vocal_members(ctx)
    member_list = [member for member in voc_members]
    embed = discord.Embed(
        title=f"Les membres en vocal sont :", description="\n", colour=discord.Colour.blue())
    for member in member_list:
        # embed.add_field(name=str(member), value="\u200b", inline=False)
        embed.add_field(name=str(member.name), value=boug_bot.dict_boug[member.id].money, inline=False)

    await ctx.send(embed=embed)

# Randomly choose a member currently inside a VoiceChannel
@boug_bot.command(description="Choisit un volontaire parmis les membre connectés en vocal")
async def volontaire(ctx):
    voc_members = get_vocal_members(ctx)
    member_list = [member.name for member in voc_members]
    volontaire = random.choice(member_list)
    embed = discord.Embed(
        title=f"<:dogekek:751132464407248986>  {volontaire} est volontaire  <:dogekek:751132464407248986>", description="", colour=discord.Colour.blue())
    await ctx.send(embed=embed)


@boug_bot.command()
async def save(ctx):
    save_bougs(boug_bot)


@boug_bot.command()
async def load(ctx):
    data_bougs = load_bougs(boug_bot)
    print('\nLoaded data: ', data_bougs)
    print('Asardoc data : ', data_bougs["265237694819467264"])
    boug_bot.loaded_data = data_bougs


# Display all members currently inside a given VoiceChannel
@boug_bot.command()
async def money(ctx): 
    embed = discord.Embed(
        title=f"Nombre de BougCoin des membres :", description="\n", colour=discord.Colour.blue())

    for boug in boug_bot.dict_boug.values():
        print(f"{boug.name}, {boug.money}")
        embed.add_field(name=boug.name, value=boug.money, inline=False)

    await ctx.send(embed=embed)


@boug_bot.command()
async def coin(ctx, target=None):
    if target:
        id_target = int(target[2:-1])
    else:
        id_target = ctx.message.author.id

    embed = discord.Embed(
        title=f"Nombre de :coin: BougCoin :coin: de :", description="\n", colour=discord.Colour.blue())
    
    target_boug = boug_bot.dict_boug[id_target]
    embed.add_field(name=target_boug.name, value=target_boug.money, inline=False)
    await ctx.send(embed=embed)


@boug_bot.command()
async def top(ctx, nth=5): 
    embed = discord.Embed(
        title=f"Top {nth} des bougs les plus riches :", description="\n", colour=discord.Colour.blue())

    sorted_dict = sorted(boug_bot.dict_boug.values(),key=lambda x: x.money, reverse=True)
    for boug in sorted_dict[:nth]:
        print(f"{boug.name}, {boug.money}")
        embed.add_field(name=boug.name, value=boug.money, inline=False)

    await ctx.send(embed=embed)

@boug_bot.command()
async def bottom(ctx, nth=5): 
    embed = discord.Embed(
        title=f"Top {nth} des bougs les plus PAUVRES (cheh) :", description="\n", colour=discord.Colour.blue())

    sorted_dict = sorted(boug_bot.dict_boug.values(),key=lambda x: x.money, reverse=False)
    for boug in sorted_dict[:nth]:
        print(f"{boug.name}, {boug.money}")
        embed.add_field(name=boug.name, value=boug.money, inline=False)
    await ctx.send(embed=embed)

"""
ADD commande admin pour créer argent (ou éditer à la main le json)
"""
@boug_bot.command()
async def give(ctx, target, amount):
    amount = int(amount)
    id_target = int(target[2:-1])
    id_author = ctx.message.author.id
    amount = min(amount, boug_bot.dict_boug[id_author].money)

    print(boug_bot.dict_boug[id_target].money)
    boug_bot.dict_boug[id_target].money = boug_bot.dict_boug[id_target].money + amount
    print(boug_bot.dict_boug[id_target].money)
    boug_bot.dict_boug[id_author].money = boug_bot.dict_boug[id_author].money - amount

    save_bougs(boug_bot)


"""
Ajouter restriction pour utiliser le bouton (seulement auteur peut cliquer)
Delete le message quand le bouton est utilisé
"""
@boug_bot.command()
async def roulboug(ctx, amount, risk=1):
    id_target = ctx.message.author.id
    amount = min(int(amount), 1000, boug_bot.dict_boug[id_target].money)
    # print(risk)
    base = 6
    
    chance = risk/base
   
    dict_gain = {0:0, 1: 0.1, 2: 0.3, 3: 0.5, 4: 0.7, 5: 1}

    print(boug_bot.dict_boug[id_target].money)
    boug_bot.dict_boug[id_target].money = boug_bot.dict_boug[id_target].money - amount - int(amount*dict_gain[risk-1])
    print(boug_bot.dict_boug[id_target].money)
    save_bougs(boug_bot)

    random_value = random.random()
    if random_value > chance:
        gain = int(amount*dict_gain[risk])
        print(boug_bot.dict_boug[id_target].money)
        boug_bot.dict_boug[id_target].money = boug_bot.dict_boug[id_target].money + amount + gain
        print(boug_bot.dict_boug[id_target].money)
        save_bougs(boug_bot)
        await ctx.send(content=f'Bravo tu as gagné {amount + gain}')
        if risk < 5:
            await roullette_button(ctx, amount, risk)
        else:
            await ctx.send(content=f'Bravo tu as gagné le max {amount + gain}')
    else:
        # boug_bot.dict_boug[id_target].money = boug_bot.dict_boug[id_target].money - loss
        await ctx.send(content=f'Dommage tu as perdu {amount}')
        save_bougs(boug_bot)

    


async def roullette_button(ctx, amount, risk):
    button_yes = Button(label="Rejouer ?", style=discord.ButtonStyle.green)
    risk += 1
    async def button_yes_callback(interaction):
        await roulboug(ctx, amount, risk)
    
    button_yes.callback = button_yes_callback

    view=View()
    view.add_item(button_yes)
    await ctx.send(view=view)


########
# @boug_bot.command()
# async def button(ctx):
#     button_yes = Button(label="yes", style=discord.ButtonStyle.green)
#     button_no = Button(label="no", style=discord.ButtonStyle.red)

#     async def button_yes_callback(interaction):
#         await ctx.send("Yes")

#     async def button_no_callback(interaction):
#         await ctx.send("No")
    
#     button_yes.callback = button_yes_callback
#     button_no.callback = button_no_callback

#     view=View()
#     view.add_item(button_yes)
#     view.add_item(button_no)
#     await ctx.send("Salut mec", view=view)

boug_bot.run(os.getenv("TOKEN"))