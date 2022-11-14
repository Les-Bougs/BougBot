import discord
from discord.ext import commands
from load_save_bougs import save_bougs, load_bougs

guild_id = [751114414132035694]

class CoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="coin", guild_ids=guild_id)
    async def coin(self, ctx, user=None):
        """Donne le solde de BougCoin d'un membre du serveur"""
        #Define target
        if user:
            id_target = int(user[2:-1])
        else:
            id_target = ctx.author.id
        target_boug = self.bot.dict_boug[id_target]

        print(id_target)

        embed = discord.Embed(
            title=f":coin: BougCoin :coin:",
            description="\n", 
            colour=discord.Colour.blue())
        embed.add_field(name="\u200b", value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:", inline=False)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="give", guild_ids=guild_id)
    async def give(self, ctx, target, amount):
        """Envoyer de l'argent à un membre du serveur"""
        amount = int(amount)
        id_target = int(target[2:-1])
        id_author = ctx.author.id
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
        await ctx.respond(embed=embed)

    @commands.slash_command(name="adgive", guild_ids=guild_id)
    async def adgive(self, ctx, target, amount):
        """! réservé au Admin ! Ajouter de l'argent à un membre du serveur"""
        list_role = [role.name for role in ctx.author.roles]
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
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(CoinCog(bot))

            