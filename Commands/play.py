import discord
import asyncio
import nacl
from discord import option
from discord.ext import commands
from load_save_bougs import save_bougs, load_bougs

guild_id = [751114414132035694]
path = "Sound/bougcast.mp3"

class PlayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="bougcast", guild_ids=guild_id)
    @discord.default_permissions(administrator=True)
    async def bougcast(self, ctx):
        """Joue le générique du BougCast"""

        user_voice = None
        user_voice = ctx.author.voice

        if user_voice != None:

            embed = discord.Embed(
                title=f"<:bougCast:836650397259137034> Boug-Cast <:bougCast:836650397259137034>",
                description="\n", 
                colour=discord.Colour.blue())
            await ctx.respond(embed=embed)

            voice_channel = user_voice.channel
            
            vc= await voice_channel.connect()
            mp3 = discord.FFmpegPCMAudio(source=path, executable='ffmpeg', pipe=False, stderr=None, before_options=None, options=None)
            vc.play(mp3)

            while vc.is_playing():
               await asyncio.sleep(1)

            vc.stop()
            await vc.disconnect()
            
        else:
            embed = discord.Embed(
                title=f":speaking_head: Tu n'es pas en vocal :speaking_head:",
                description="\n", 
                colour=discord.Colour.blue())
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(PlayCog(bot))