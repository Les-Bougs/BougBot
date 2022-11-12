import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random

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

    async def on_ready(self):
        self.botid = f"<@{self.user.id}>"
        print(f"{self.user.display_name} est prêt.")

    async def reply(self, message, list_words, response):
        if any(x in message.content.lower() for x in list_words):
            if self.botid in message.content:
                user = message.author
                await message.reply(f"{response} <@{user.id}>")

    async def on_message(self, message):
        await self.reply(message, ("merci","cimer","thanks","thx"), "De rien")
        await self.reply(message, ("salut","hello","wesh","bonjour"), "Salut")
        await self.reply(message, ("ntm","fdp","merde","putain"), "Attention à ton langage ;-)")
        await self.process_commands(message)


def get_vocal_members(ctx, channel_name="Général"):
    return discord.utils.get(ctx.guild.channels, name=channel_name).members


boug_bot = BougBot()

# Custom bot commands below

# Display all members currently inside a given VoiceChannel
@boug_bot.command()
async def voclist(ctx):
    voc_members = get_vocal_members(ctx)
    member_list = [member.name for member in voc_members]
    embed = discord.Embed(
        title=f"Les membres en vocal sont :", description=member_list, colour=discord.Colour.blue())
    for x in member_list:
        embed.add_field(name=member_list[x+1], value="", inline=False)
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



boug_bot.run(os.getenv("TOKEN"))