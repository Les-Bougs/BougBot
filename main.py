import os
import discord
import random
import datetime
from dotenv import load_dotenv

from Bougs import Boug
from load_save_bougs import save_bougs, load_bougs
from voice_update import voice_update

load_dotenv(dotenv_path="config")

class BougBot(discord.Bot):
    def __init__(self):
        self.dict_boug = {}
        self.guild_id = [751114414132035694]

        super().__init__(
            intents=discord.Intents.all(),
            description="BougBot, ton nouveau meilleur pote !",
            case_insensitive=True,
        )

    async def on_ready(self):
        self.botid = f"<@{self.user.id}>"
        self.name = f"{self.user.display_name}"
        self.list_members_guild = list(discord.utils.get(self.guilds, name="Les Bougs du fond").members)
        self.loaded_data = load_bougs()

        for guild_member in self.list_members_guild:
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
        print(f"{self.name} est prêt.\nBot id: {self.botid}")

    async def on_message(self, message):
        async def reply(self, message, list_words, response):
            if any(x in message.content.lower() for x in list_words):
                if self.botid in message.content:
                    user = message.author
                    await message.reply(f"{response} <@{user.id}>")
        await reply(self, message, ("merci","cimer","thanks","thx"), "De rien")
        await reply(self, message, ("salut","hello","wesh","bonjour"), "Salut")
        await reply(self, message, ("ntm","fdp","merde","putain","tg"), "Attention à ton langage ;-)")
        print(message.content)

    async def on_voice_state_update(self, member, before, after):
        voice_update(self, member, before, after)
    
bot = BougBot()

bot.load_extension("Commands.coin")

bot.run(os.getenv("TOKEN"))