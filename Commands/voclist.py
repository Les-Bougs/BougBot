import discord
from discord.ext import commands
import random

guild_id = [751114414132035694]


class VoclistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="voclist", guild_ids=guild_id)
    async def voclist(self, ctx):
        """Affiche les membres actuelement connectés en vocal"""

        voc_members = get_vocal_members(ctx)

        if voc_members != []:
            member_list = [member for member in voc_members]
            embed = discord.Embed(
                title=f":speaking_head: Membres en vocal :speaking_head:",
                description="\n",
                colour=discord.Colour.blue(),
            )
            for member in member_list:
                embed.add_field(name="\u200b", value=f"<@{member.id}>", inline=False)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Personne en vocal :cry:",
                description="\n",
                colour=discord.Colour.blue(),
            )
            await ctx.respond(embed=embed)

    @commands.slash_command(name="volontaire", guild_ids=guild_id)
    async def volontaire(self, ctx):
        """Choisit un volontaire parmis les membres connectés en vocal"""

        voc_members = get_vocal_members(ctx)

        if voc_members != []:
            member_list = [member.name for member in voc_members]
            volontaire = random.choice(member_list)
            embed = discord.Embed(
                title=f"<:dogekek:751132464407248986>  {volontaire} est volontaire  <:dogekek:751132464407248986>",
                description="\n",
                colour=discord.Colour.blue(),
            )
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(
                title=f"Personne en vocal :cry:",
                description="\n",
                colour=discord.Colour.blue(),
            )
            await ctx.respond(embed=embed)


def get_vocal_members(ctx, channel_name="Général"):
    """Return all member conected in "channel_name" voice channel"""
    return discord.utils.get(ctx.guild.channels, name=channel_name).members


def setup(bot):
    bot.add_cog(VoclistCog(bot))
