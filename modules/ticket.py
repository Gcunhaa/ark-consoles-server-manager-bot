
from os import name
from .base import Base
from discord.ext import commands
from discord import Embed, Guild, PermissionOverwrite
from core import settings



class Ticket(Base):
    
    def load_module_event(self):
        self.message_id = {}
        self.role_id = {}

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        #Create text channel when joins the server
        await self.create_text_channel(guild)

    @commands.Cog.listener()
    async def on_ready(self):
        #Verify if every server has the channel and if not create 
        for guild in self.bot.guilds:
            await self.create_text_channel(guild)

    """[summary]
    
    Listener responsible for waiting for reaction, and when happens create the ticket.
    
    """

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        guild_id = reaction.message.guild.id
        message_id = reaction.message.id
        
        #verify if user is bot
        if user.bot:
            return

        if self.message_id[guild_id] == message_id:
            await reaction.message.remove_reaction(member=user, emoji=reaction.emoji)

            if reaction.emoji == settings.get_ticket_create_emoji() :
                guild = reaction.message.guild

                #Set @everyone permissions
                default_overwrite = PermissionOverwrite()
                default_overwrite.send_messages = False
                default_overwrite.read_messages = False

                channel = await guild.create_text_channel(name=f"ticket-{user.name}")
                
                #Set permissions for user and suport role
                overwrite = PermissionOverwrite()
                overwrite.send_messages = True
                overwrite.read_messages = True

                suport_team_role = guild.get_role(self.role_id[guild.id])

                await channel.set_permissions(target=guild.default_role, overwrite=default_overwrite)
                await channel.set_permissions(target=suport_team_role,overwrite=overwrite)
                await channel.set_permissions(target=user, overwrite=overwrite)

                await channel.send(user.mention)
        
                #Close support embed
                embed = Embed(title=settings.get_ticket_close_embed_title(), description=settings.get_ticket_close_embed_description())
                embed.set_footer(text=settings.get_ticket_close_embed_footer(), icon_url=self.bot.user.avatar_url)
                embed.colour = int(settings.get_ticket_close_embed_color(),16)

                message = await channel.send(embed=embed)
                await message.add_reaction(emoji=settings.get_ticket_close_emoji())
    
        if 'ticket-' in reaction.message.channel.name:
            if reaction.emoji == settings.get_ticket_close_emoji():
                await reaction.message.channel.delete()

    """[summary]
    
    Method responsible for creating the channel if not exist
    
    """
    
    async def create_text_channel(self, guild : Guild) -> int:
        channel_global = None

        exist = False           
        for channel in guild.channels:
            if str(channel) == settings.get_ticket_channel_name(): 
                exist = True
                channel_global = channel

                break
            
        #If channel doesnt exist create one
        if not exist:
            channel = await guild.create_text_channel(settings.get_ticket_channel_name())


            overwrite = PermissionOverwrite()
            overwrite.send_messages = False
            overwrite.read_messages = True

            everyone_role = guild.default_role

            await channel.set_permissions(target=everyone_role,overwrite=overwrite)
            channel_global = channel
        
        await channel_global.purge()
        
        embed = Embed(title=settings.get_ticket_embed_title(), description=settings.get_ticket_embed_description())
        embed.set_footer(text=settings.get_ticket_embed_footer(), icon_url=self.bot.user.avatar_url)
        embed.colour = int(settings.get_ticket_embed_color(),16)

        message = await channel_global.send(embed=embed)
        
        self.message_id[guild.id] = message.id

        #Get role id
        for role in guild.roles:
            if str(role) == settings.get_ticket_suport_role():
                self.role_id[guild.id] = role.id

        await message.add_reaction(settings.get_ticket_create_emoji())

        return channel_global.id
        