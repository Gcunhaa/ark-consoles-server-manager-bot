from .base import Base
from core.servers import servers
from discord import Embed
from discord.ext import commands


class Reload(Base):
    

    @commands.command(pass_context=True)
    async def reload(self, ctx, module_name: str):
        """Reload module data based on the name

        Args:
            ctx ([type]): [description]
            ticketpanel_name (str): the name of the ticketpanel that you want to generate
        """
        licence_id = await servers.get_licence_id(ctx.guild.id)
        cog = self.bot.get_cog(module_name)

        embed = Embed(title='Module Reload')
        embed.set_footer(text='Ark Consoles Server Manager', icon_url=self.bot.user.avatar_url)

        if not cog:
            
            embed.description = f"Module **{module_name}** doesnt exist.\nCheck your spelling and remember to use capital letters."
            await ctx.send(embed=embed)
            return
        
        await cog.reload_cog(licence_id)
        embed.description = f'Data from **{module_name}** reloaded with success.'
        await ctx.send(embed=embed)
