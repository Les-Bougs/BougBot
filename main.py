import os
import discord
from discord.ui import Button, View
from discord.ext import commands
from dotenv import load_dotenv
import random
import datetime
import json

from Bougs import Boug
from load_save_bougs import save_bougs, load_bougs
from voice_update import voice_update

from Commands.coin import CoinCog
from Commands.money import MoneyCog
from Commands.voclist import VoclistCog
from Commands.game import GameCog

# import Commands.coin_cog as coin_cog

load_dotenv(dotenv_path="config")
guild_id = discord.Object(id=751114414132035694)

class BougBot(commands.Bot):
    def __init__(self):
        self.description = """Boug Bot, ton nouveau meilleur pote"""

        super().__init__(
            command_prefix=("!"),
            intents=discord.Intents.all(),
            description=self.description,
            case_insensitive=True,
        )

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    async def on_ready(self):
        # add commands from Cogs
        await self.add_cog(CoinCog(self))
        await self.add_cog(MoneyCog(self))
        await self.add_cog(VoclistCog(self))
        await self.add_cog(GameCog(self))
        # end add commands
        self.botid = f"<@{self.user.id}>"
        await self.tree.sync(guild=guild_id)
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
                    self.loaded_data[id_member]['money'],
                    self.loaded_data[id_member]['last_connected']
                )
            else:
                self.dict_boug[guild_member.id] = Boug(
                    guild_member.id,
                    guild_member.name,
                    random.randint(0,1000),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
        save_bougs(self)

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

    async def on_voice_state_update(self, member, before, after):
        voice_update(self, member, before, after)
    

boug_bot = BougBot()


@boug_bot.tree.command(name = "test", description = "C'est un test lol", guild=guild_id)
async def test(interaction):
    await interaction.response.send_message("Test!")

@boug_bot.tree.command(name = "test2", description = "C'est un test lol 2", guild=guild_id)
async def test2(interaction, arg: str='Default arg'):
    await interaction.response.send_message(f"Test! {arg}")


# Custom bot commands below
@boug_bot.command()
async def save(ctx):
    save_bougs(boug_bot)


@boug_bot.command()
async def load(ctx):
    data_bougs = load_bougs(boug_bot)
    print('\nLoaded data: ', data_bougs)
    boug_bot.loaded_data = data_bougs


boug_bot.run(os.getenv("TOKEN"))