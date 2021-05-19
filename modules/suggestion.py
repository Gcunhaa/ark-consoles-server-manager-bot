from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed, Guild
from models.module import Module
from core.channel import Channels
from core.servers import servers
from models.channel import Channel

class Suggestion(Base):

    @commands.Cog.listener()
    async def on_ready(self):
        module_name = 'Suggestion'
        channel_name = "Suggestion Channel"
        
        module = await Module.query.where(Module.name == module_name).gino.first()

        if not module:
            module = await Module.create(name=module_name)

        
        channel = await Channel.query.where(Channel.name == channel_name).where(Channel.module_id == module.id).gino.first()
        if not channel:
            channel = await Channel.create(name=channel_name, module_id=module.id)
            

        self.channels = Channels(channel.id,785526951758397450)
        await servers.get_server_id(10)

    """
        Command suggest, makes suggestion
    """
    @commands.command()
    async def suggest(self, ctx, *args):
        licence_id = await servers.get_licence_id(ctx.guild.id)
        channel = ctx.guild.get_channel(await self.channels.get_channel_id(licence_id))
        embed = settings.get_suggestion_core_embed()
        embed.set_footer(text=embed.footer.text.format(username=ctx.author), icon_url=self.bot.user.avatar_url)

    
        if len(args) == 0:
            embed.description = "Wrong syntax, try **-suggest <text>**"
            await ctx.send(embed=embed)
            return

        embed.description = ' '.join(args)
        await ctx.message.delete()
        message = await channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')


    async def reload_cog(self, licence_id: int):
        await self.channels.update_channel_id(licence_id)
