import discord
from discord import option
from discord.ext import commands
from discord.ui import Button, View
from load_save_bougs import save_bougs, load_bougs

import random

guild_id = [751114414132035694]


class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="roulboug", guild_ids=guild_id)
    @option("amount", description="montant à mettre en jeu", min_value=1)
    async def roulboug(self, ctx, amount: int, risk=1):
        """Permet de jouer au célèbre RoulBoug"""

        async def roullette_button(self, ctx, amount, risk, id_target, view):
            button_yes = Button(label="Rejouer ?", style=discord.ButtonStyle.green)
            risk += 1

            async def button_yes_callback(interaction):
                if interaction.user.id == id_target:
                    await interaction.message.delete()
                    await self.roulboug(ctx, amount, risk)

            button_yes.callback = button_yes_callback
            view.add_item(button_yes)

        id_target = ctx.author.id
        if self.bot.dict_boug[id_target].money == 0:
            await ctx.respond("T'es à sec fréro, déso")
            return None

        amount = min(amount, 1000, self.bot.dict_boug[id_target].money)
        base = 6
        chance = risk / base
        # view=View(timeout=30) # add timeout to roulboug button
        view = View()

        # Tableau des gains
        dict_gain = {0: 0, 1: 0.1, 2: 0.3, 3: 0.5, 4: 0.7, 5: 1}

        # On retire la mise de départ
        self.bot.dict_boug[id_target].money = (
            self.bot.dict_boug[id_target].money
            - amount
            - int(amount * dict_gain[risk - 1])
        )
        save_bougs(self.bot)

        embed = discord.Embed(
            title=f":hot_face: <:handgun:833364124024307732>  Roulboug  <:handgunL:836656077856440370> :hot_face:",
            description=f"BougCoin mis en jeu: {amount} :coin:",
            colour=discord.Colour.blue(),
        )

        random_value = random.random()
        if random_value > chance:  # when player wins
            gain = int(amount * dict_gain[risk])
            self.bot.dict_boug[id_target].money = (
                self.bot.dict_boug[id_target].money + amount + gain
            )
            save_bougs(self.bot)
            embed.add_field(
                name="\u200b",
                value=f":tada: Bravo <@{self.bot.dict_boug[id_target].id}> tu as gagné {amount + gain} :coin:",
                inline=False,
            )
            if risk < 5:
                await roullette_button(self, ctx, amount, risk, id_target, view)
                if risk > 1:
                    await ctx.send(embed=embed, view=view)
                else:
                    await ctx.respond(embed=embed, view=view)
            else:
                embed.add_field(
                    name="\u200b",
                    value=f"<:stonks:833364123990360075> Bravo champion, tu as gagné le jackpot !",
                    inline=False,
                )
                await ctx.send(embed=embed)
        else:  # when player lose
            botid_clean = int(self.bot.botid[2:-1])
            self.bot.dict_boug[botid_clean].money = (
                self.bot.dict_boug[botid_clean].money + amount
            )  # envoi la somme perdue à BougBot
            save_bougs(self.bot)
            embed.add_field(
                name="\u200b",
                value=f"<:feelsBadMan:751132464394534942> Dommage <@{self.bot.dict_boug[id_target].id}> tu as perdu {amount} :coin:",
                inline=False,
            )
            if risk > 1:
                await ctx.send(embed=embed)
            else:
                await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(GameCog(bot))
