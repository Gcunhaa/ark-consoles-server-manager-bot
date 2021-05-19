from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed
from random import randint

class Flip(Base):

    """
        Command flip, flips a coin heads or tails
    """
    @commands.command()
    async def flip(self, ctx):
        choice = randint(0,1)
        embed = Embed()
        embed.set_footer(text='Ark Consoles Server Manager', icon_url=self.bot.user.avatar_url)

        if choice == 0:
            embed.description = "You got **heads**!"
        elif choice == 1:
            embed.description = "You got **tails**!"
        await ctx.send(embed=embed)