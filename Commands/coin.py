import discord
from discord.ext import commands

class CoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def coin(self, ctx, target=None):
        if target:
            id_target = int(target[2:-1])
        else:
            id_target = ctx.message.author.id

        embed = discord.Embed(
            title=f"Nombre de :coin: BougCoin :coin: de :", description="\n", colour=discord.Colour.blue())
        
        target_boug = self.bot.dict_boug[id_target]
        embed.add_field(name=target_boug.name, value=target_boug.money, inline=False)
        await ctx.send(embed=embed)