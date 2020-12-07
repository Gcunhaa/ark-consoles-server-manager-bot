from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed

class Links(Base):

    """
        Command links, return embed with links
    """
    @commands.command()
    async def links(self, ctx):
        embed = Embed(title=settings.get_link_embed_title())
        embed.set_footer(text=settings.get_link_embed_footer(), icon_url=self.bot.user.avatar_url)
        embed.colour = int(settings.get_link_embed_color(), 16)

        link_dict = settings.get_link_dict()
        
        for title in link_dict:
            embed.add_field(name=title,value=link_dict.get(title))

        await ctx.send(embed=embed)