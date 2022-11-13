import discord
from discord.ext import commands
from load_save_bougs import save_bougs, load_bougs


guild_id = discord.Object(id=751114414132035694)

class CoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # @nextcord.slash_command(name = "coin", description = "Donne le solde de BougCoin de nimporte qui sur le serveur", guild_ids=[guild_id])
    @commands.command()
    async def coin(self, ctx, target=None):
        #Define target
        if target:
            id_target = int(target[2:-1])
        else:
            id_target = ctx.message.author.id
        target_boug = self.bot.dict_boug[id_target]

        embed = discord.Embed(
            title=f":coin: BougCoin :coin:",
            description="\n", 
            colour=discord.Colour.blue())
        embed.add_field(name="\u200b", value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:", inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def give(self, ctx, target, amount):
        amount = int(amount)
        id_target = int(target[2:-1])
        id_author = ctx.message.author.id
        target_boug = self.bot.dict_boug[id_target]
        author_boug = self.bot.dict_boug[id_author]
        amount = min(amount, author_boug.money)
        amount = max(amount, 0)

        #Transaction
        target_boug.money += amount
        author_boug.money -= amount
        save_bougs(self.bot)

        embed = discord.Embed(
            title=f":coin: BougCoin :coin:", 
            description="\n", 
            colour=discord.Colour.blue())
        embed.add_field(name="\u200b", value=f"<@{author_boug.id}> :arrow_right: <@{target_boug.id}>: {amount} :coin:", inline=False)
        embed.add_field(name="\u200b", value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:", inline=False)
        embed.add_field(name="\u200b", value=f":bank: <@{author_boug.id}>: {author_boug.money} :coin:", inline=False)
        await ctx.reply(embed=embed)

    @commands.command()
    async def adgive(self, ctx, target, amount):
        list_role = [role.name for role in ctx.message.author.roles]
        if "admin" in list_role:
            amount = int(amount)
            id_target = int(target[2:-1])
            target_boug = self.bot.dict_boug[id_target]

            #Transaction
            target_boug.money += amount
            save_bougs(self.bot)

            embed = discord.Embed(
                title=f":coin: BougCoin :coin:", 
                description="\n", 
                colour=discord.Colour.blue())
            embed.add_field(name="\u200b", value=f":moneybag: :arrow_right: <@{target_boug.id}>: {amount} :coin:", inline=False)
            embed.add_field(name="\u200b", value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:", inline=False)
            await ctx.reply(embed=embed)

            