import discord
from discord.ext import commands
from discord.ui import Button, View
from load_save_bougs import save_bougs, load_bougs

import random

class GameCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    Ajouter restriction pour utiliser le bouton (seulement auteur peut cliquer)
    Delete le message quand le bouton est utilisé
    """
    @commands.command()
    async def roulboug(self, ctx, amount, risk=1):
        id_target = ctx.message.author.id
        amount = min(int(amount), 1000, self.bot.dict_boug[id_target].money)
        # print(risk)
        base = 6
        
        chance = risk/base
    
        dict_gain = {0:0, 1: 0.1, 2: 0.3, 3: 0.5, 4: 0.7, 5: 1}

        print(self.bot.dict_boug[id_target].money)
        self.bot.dict_boug[id_target].money = self.bot.dict_boug[id_target].money - amount - int(amount*dict_gain[risk-1])
        print(self.bot.dict_boug[id_target].money)
        save_bougs(self.bot)

        random_value = random.random()
        if random_value > chance:
            gain = int(amount*dict_gain[risk])
            print(self.bot.dict_boug[id_target].money)
            self.bot.dict_boug[id_target].money = self.bot.dict_boug[id_target].money + amount + gain
            print(self.bot.dict_boug[id_target].money)
            save_bougs(self.bot)
            await ctx.send(content=f'Bravo tu as gagné {amount + gain}')
            if risk < 5:
                await self.roullette_button(ctx, amount, risk)
            else:
                await ctx.send(content=f'Bravo tu as gagné le max {amount + gain}')
        else:
            # self.bot.dict_boug[id_target].money = self.bot.dict_boug[id_target].money - loss
            await ctx.send(content=f'Dommage tu as perdu {amount}')
            save_bougs(self.bot)
    

    async def roullette_button(self, ctx, amount, risk):
        button_yes = Button(label="Rejouer ?", style=discord.ButtonStyle.green)
        risk += 1
        async def button_yes_callback(interaction):
            await self.roulboug(ctx, amount, risk)
        
        button_yes.callback = button_yes_callback

        view=View()
        view.add_item(button_yes)
        await ctx.send(view=view)