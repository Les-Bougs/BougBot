import discord
from discord.ext import commands

class MoneyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def money(self, ctx): 
        embed = discord.Embed(
            title=f"Nombre de BougCoin des membres :", description="\n", colour=discord.Colour.blue())

        for boug in self.bot.dict_boug.values():
            print(f"{boug.name}, {boug.money}")
            embed.add_field(name=boug.name, value=boug.money, inline=False)

        await ctx.send(embed=embed)
    
    @commands.command()
    async def top(self, ctx, nth=5): 
        embed = discord.Embed(
            title=f"Top {nth} des bougs les plus riches :", description="\n", colour=discord.Colour.blue())

        sorted_dict = sorted(self.bot.dict_boug.values(),key=lambda x: x.money, reverse=True)
        for boug in sorted_dict[:nth]:
            print(f"{boug.name}, {boug.money}")
            embed.add_field(name=boug.name, value=boug.money, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def bottom(self, ctx, nth=5): 
        embed = discord.Embed(
            title=f"Top {nth} des bougs les plus PAUVRES (cheh) :", description="\n", colour=discord.Colour.blue())

        sorted_dict = sorted(self.bot.dict_boug.values(),key=lambda x: x.money, reverse=False)
        for boug in sorted_dict[:nth]:
            print(f"{boug.name}, {boug.money}")
            embed.add_field(name=boug.name, value=boug.money, inline=False)
        await ctx.send(embed=embed)