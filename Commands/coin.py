import discord
from discord import option
from discord.ext import commands
from load_save_bougs import save_bougs, load_bougs

guild_id = [751114414132035694]


class CoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="coin", guild_ids=guild_id)
    @option("user", description="Membre du serveur, commence par @")
    @option("display", description="Rendre le resultat visible pour tout le monde", choices=["False", "True"])
    async def coin(self, ctx, user=None, display: bool=False):
        """Donne le solde de BougCoin d'un membre du serveur"""

        # Target
        if user:
            id_target = int(user[2:-1])
        else:
            id_target = ctx.author.id
        target_boug = self.bot.dict_boug[id_target]

        # Embed
        embed = discord.Embed(
            title=f":coin: BougCoin :coin:",
            description="\n",
            colour=discord.Colour.blue(),
        )
        embed.add_field(
            name="\u200b",
            value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:",
            inline=False,
        )
        await ctx.respond(embed=embed, ephemeral=not(display))

    @commands.slash_command(name="give", guild_ids=guild_id)
    @option("user", description="Membre du serveur, commence par @")
    @option("amount", description="Montant de BougCoin à crediter", min_value=1)
    async def give(self, ctx, user: str, amount: int):
        """Envoyer de l'argent à un membre du serveur"""

        # Target & Author
        id_target = int(user[2:-1])
        id_author = ctx.author.id
        target_boug = self.bot.dict_boug[id_target]
        author_boug = self.bot.dict_boug[id_author]
        amount = min(amount, author_boug.money)

        # Transaction
        target_boug.money += amount
        author_boug.money -= amount
        save_bougs(self.bot)

        # Embed
        embed = discord.Embed(
            title=f":coin: BougCoin :coin:",
            description="\n",
            colour=discord.Colour.blue(),
        )
        embed.add_field(
            name="\u200b",
            value=f"<@{author_boug.id}> :arrow_right: <@{target_boug.id}>: {amount} :coin:",
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:",
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value=f":bank: <@{author_boug.id}>: {author_boug.money} :coin:",
            inline=False,
        )
        await ctx.respond(embed=embed)

    @commands.slash_command(name="adgive", guild_ids=guild_id)
    @discord.default_permissions(
        administrator=True
    )  # Seul les admin peuvent faire la command TODO à test
    @option("user", description="Membre du serveur, commence par @")
    @option("amount", description="Montant de BougCoin à crediter")
    @option("display", description="Rendre le resultat visible pour tout le monde", choices=["False", "True"])
    async def adgive(self, ctx, target: str, amount: int, display: bool=False):
        """! réservé aux Admins ! Ajouter de l'argent à un membre du serveur"""

        # Target
        id_target = int(target[2:-1])
        target_boug = self.bot.dict_boug[id_target]

        # Transaction
        target_boug.money += amount
        save_bougs(self.bot)

        # Embed
        embed = discord.Embed(
            title=f":coin: BougCoin :coin:",
            description="\n",
            colour=discord.Colour.blue(),
        )
        embed.add_field(
            name="\u200b",
            value=f":moneybag: :arrow_right: <@{target_boug.id}>: {amount} :coin:",
            inline=False,
        )
        embed.add_field(
            name="\u200b",
            value=f":bank: <@{target_boug.id}>: {target_boug.money} :coin:",
            inline=False,
        )
        await ctx.respond(embed=embed, ephemeral=not(display))


def setup(bot):
    bot.add_cog(CoinCog(bot))
