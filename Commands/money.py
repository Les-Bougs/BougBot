import discord
from discord.ext import commands

guild_id = [751114414132035694]

class MoneyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="money", guild_ids=guild_id)
    async def money(self, ctx): 
        embed = discord.Embed(
            title=f":coin: BougCoin :coin:", 
            description="\n", 
            colour=discord.Colour.blue())
        for boug in self.bot.dict_boug.values():
            embed.add_field(name="\u200b", value=f":bank: {boug.name}: {boug.money} :coin:", inline=False)

        await ctx.respond(embed=embed)
    
    @commands.slash_command(name="top", guild_ids=guild_id) # TO DO add aliases
    async def top(self, ctx, nth:int=5):
        sorted_dict = sorted(self.bot.dict_boug.values(),key=lambda x: x.money, reverse=True)

        embed = discord.Embed(
            title=f":chart_with_upwards_trend: Top {nth} des bougs les plus riches :", 
            description="\n", 
            colour=discord.Colour.blue())
        for boug in sorted_dict[:nth]:
            embed.add_field(name="\u200b", value=f":bank: {boug.name}: {boug.money} :coin:", inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command(name="bottom", guild_ids=guild_id)
    async def bottom(self, ctx, nth=5):
        sorted_dict = sorted(self.bot.dict_boug.values(),key=lambda x: x.money, reverse=False)

        embed = discord.Embed(
            title=f":chart_with_downwards_trend: Top {nth} des bougs les plus PAUVRES:", 
            description="\n", 
            colour=discord.Colour.blue())
        for boug in sorted_dict[:nth]:
            print(f"{boug.name}, {boug.money}")
            embed.add_field(name="\u200b", value=f":bank: {boug.name}: {boug.money} :coin:", inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(MoneyCog(bot))