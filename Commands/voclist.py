import discord
from discord.ext import commands
import random

guild_id = [751114414132035694]

class VoclistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="voclist", guild_ids=guild_id)
    async def voclist(self, ctx):
        """Display all members currently inside a given VoiceChannel"""
        voc_members = get_vocal_members(ctx)
        member_list = [member for member in voc_members]
        embed = discord.Embed(
            title=f"Les membres en vocal sont :", description="\n", colour=discord.Colour.blue())
        for member in member_list:
            # embed.add_field(name=str(member), value="\u200b", inline=False)
            embed.add_field(name=str(member.name), value=self.bot.dict_boug[member.id].money, inline=False)

        await ctx.respond(embed=embed)

    @commands.slash_command(name="volontaire", guild_ids=guild_id)
    async def volontaire(self, ctx):
        """Choisit un volontaire parmis les membre connectés en vocal"""
        voc_members = get_vocal_members(ctx)
        member_list = [member.name for member in voc_members]
        volontaire = random.choice(member_list)
        embed = discord.Embed(
            title=f"<:dogekek:751132464407248986>  {volontaire} est volontaire  <:dogekek:751132464407248986>", description="", colour=discord.Colour.blue())
        await ctx.respond(embed=embed)

def get_vocal_members(ctx, channel_name="Général"):
    return discord.utils.get(ctx.guild.channels, name=channel_name).members

def setup(bot):
    bot.add_cog(VoclistCog(bot))