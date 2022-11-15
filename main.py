import os
import discord
import random
import datetime
from dotenv import load_dotenv

from Bougs import Boug
from load_save_bougs import save_bougs, load_bougs
from voice_update import voice_update
from reaction_update import reaction_update

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
        self.dict_msg = {}
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
                    #random.randint(0,1000),
                    0,
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
    
    # ADD ON REACTION EVENT
    async def on_reaction_add(self, reaction, user):
        reaction_update(self, reaction, user)
    
## ADD JOB EVERY X TIMES
# import datetime
# import discord
# from discord.ext import tasks

# client = discord.Client()

# goodNightTime = datetime.time(hour=21, minute=45, second=40) #Create the time on which the task should always run

# @tasks.loop(time=goodNightTime) #Create the task
# async def Goodnight():
#     channel = client.get_channel(806702411808768023)
#     await channel.send("Good night! Make sure to go to sleep early, and get enough sleep!")
#     print("Night Working")

# @client.event
# async def on_ready():
#     if not Goodnight.is_running():
#         Goodnight.start() #If the task is not already running, start it.
#         print("Good night task started")

# client.run(TOKEN)


bot = BougBot()

bot.load_extension("Commands.coin")
bot.load_extension("Commands.money")
bot.load_extension("Commands.voclist")
bot.load_extension("Commands.game")

bot.run(os.getenv("TOKEN"))