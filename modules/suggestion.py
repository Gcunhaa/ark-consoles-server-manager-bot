
from os import name
from .base import Base
from discord.ext import commands
from discord import Embed, Guild, PermissionOverwrite
from core import settings



class Suggestion(Base):
    
    def load_module_event(self):
        self.channel_id = {}

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        #Create text channel when joins the server
        channel_id = await self.create_text_channel(guild)
        self.channel_id[guild.id] = channel_id

    @commands.Cog.listener()
    async def on_ready(self):
        #Verify if every server has the channel and if not create 
        for guild in self.bot.guilds:
            channel_id = await self.create_text_channel(guild)
            self.channel_id[guild.id] = channel_id


    """

        suggest command for creating suggestions

    """
    @commands.command(pass_context=True)
    async def suggest(self, ctx, *args):
        channel = self.bot.get_channel(self.channel_id[ctx.guild.id])
        username = ctx.author.name

        #Verify if has any text at all
        if len(args) == 0:
            embed = Embed(title=settings.get_suggestion_syntax_embed_title(), description=settings.get_suggestion_syntax_embed_description())
            embed.set_footer(text=settings.get_suggestion_syntax_embed_footer(), icon_url=self.bot.user.avatar_url)
            embed.colour = int(settings.get_suggestion_syntax_embed_color(), 16)
            await ctx.send(embed=embed)
            return
        
        #Verify if server has the proper channel
        if not channel:
            await ctx.send('Command not working properly, please contact the developer. Error: 01')
            return
        

        embed = Embed(title=settings.get_suggestion_embed_title(), description=' '.join(args))
        embed.set_footer(text=settings.get_suggestion_embed_footer().format(username=username), icon_url=ctx.author.avatar_url)
        embed.colour = int(settings.get_suggestion_embed_color(), 16)

        await ctx.message.delete()
        message = await channel.send(embed=embed)

        await message.add_reaction('✅')
        await message.add_reaction('❌')

    """[summary]
    
    Method responsible for creating the channel if not exist
    
    """
    
    async def create_text_channel(self, guild : Guild) -> int:
        channel_id = 0
        exist = False           
        for channel in guild.channels:
            if str(channel) == settings.get_suggestion_channel_name(): 
                exist = True
                channel_id = channel.id
                break
            
        #If channel doesnt exist create one
        if not exist:
            channel = await guild.create_text_channel(settings.get_suggestion_channel_name())
            channel_id = channel.id

            overwrite = PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.read_messages = True

            everyone_role = guild.default_role

            await channel.set_permissions(target=everyone_role,overwrite=overwrite)
        return channel_id
        