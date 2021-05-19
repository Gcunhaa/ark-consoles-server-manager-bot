from .base import Base
from discord.ext import commands
from core import settings
from core.servers import servers
from discord import Embed, Member
from random import randint
from models.gif import Gif

class Slap(Base):

    """
        Command slap, slaps given user with a randomly chosen gif
    """
    @commands.command()
    async def slap(self, ctx, member : Member):
        licence_id = await servers.get_licence_id(ctx.guild.id)
        #TODO: Make gets random row
        gif = await Gif.query.where(Gif.licence_id == licence_id).gino.first()
        print(gif.value)
        
        if gif:
            embed = Embed()
            embed.set_image(url=gif.value)
            embed.set_footer(text='Ark Consoles Server Manager', icon_url=self.bot.user.avatar_url)
            await ctx.send(content=f':clap: {ctx.author.mention} slapped {member.mention}',embed=embed)