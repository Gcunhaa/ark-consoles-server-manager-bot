from models import licence
from models.role import Role
from core.role import Roles
from models import server
from models.module import Module
from .base import Base
from discord.ext import commands
from discord import Embed, TextChannel, CategoryChannel, Member, Guild, PermissionOverwrite
from models.ticketpanel import Ticketpanel
from models.category import Category
from core.category import Categorys
from core.servers import servers
from core import settings


class Ticket(Base):

    @commands.Cog.listener()
    async def on_ready(self):
        module = await Module.query.where(Module.name == 'Ticket').gino.first()

        if not module:
            module = await Module.create(name='Ticket')
            category = await Category.create(name='Ticket Category', module_id=module.id)
            role = await Role.create(name='Support Role', module_id=module.id)
        else:
            category = await Category.query.where(Category.name == 'Ticket Category').where(Category.module_id == module.id).gino.first()
            if not category:
                category = await Category.create(name='Ticket Category', module_id=module.id)

            role = await Role.query.where(Role.name == 'Support Role').where(Role.module_id == module.id).gino.first()
            if not role:
                role = await Role.create(name='Support Role', module_id=module.id)

        category_id = category.id
        role_id = role.id
        self.categorys: Categorys = Categorys(
            category_id=category_id, default_id=785854511524216862)
        self.roles: Roles = Roles(
            role_id=role_id, default_id=784514780554985572)
        await servers.get_server_id(10)

    async def check_if_has_permission(ctx):
        """Check if user has permission for command

        """
        licence_id = await servers.get_licence_id(ctx.guild.id)
        role_id = await ctx.bot.get_cog('Ticket').roles.get_role_id(licence_id)
        author = ctx.author
        role = ctx.guild.get_role(role_id)
        return role in author.roles
    
    async def check_if_is_ticket(ctx):
        """Check if command was issued inside a ticket

        """
        channel : TextChannel = ctx.channel
        return 'ticket-' in channel.name


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """

        Listen to the reactions, and verify if its a ticket panel

        """
        emoji = str(payload.emoji)
        member = payload.member

        if member.bot:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if emoji != settings.get_ticket_create_emoji():
            return
    
        if len(message.embeds) == 0 or message.embeds[0].title != settings.get_ticket_panel_embed().title:
            return
        
        await message.remove_reaction(emoji, member)
        await self.create_ticket(member,message.guild)


    @commands.command(pass_context=True)
    @commands.check(check_if_has_permission)
    async def ticket(self, ctx, ticketpanel_name: str):
        """Create ticketpanel based on the name

        Args:
            ctx ([type]): [description]
            ticketpanel_name (str): the name of the ticketpanel that you want to generate
        """
        licence_id = servers.get_licence_id(ctx.guild.id)
        ticketpanel: Ticketpanel = await Ticketpanel.query.where(Ticketpanel.name == ticketpanel_name).where(Ticketpanel.licence_id == licence_id).gino.first()

        if not ticketpanel:
            embed: Embed = settings.get_ticket_error_embed()
            embed.description = f"\nTicketPanel called **{ticketpanel_name}** doesnt exist\n"
            embed.set_footer(text=embed.footer.text,
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return

        embed : Embed = settings.get_ticket_panel_embed()
        embed.description = ticketpanel.description
        embed.set_footer(text=embed.footer.text,
                         icon_url=self.bot.user.avatar_url)
        await ctx.message.delete()
        message = await ctx.send(embed=embed)
        await message.add_reaction(settings.get_ticket_create_emoji())

    @ticket.error
    async def ticket_error(self, ctx, error):
        """ Handles errors caused in the ticket command 
        """
        embed: Embed = settings.get_ticket_error_embed()

        embed.set_footer(text=embed.footer.text,
                         icon_url=self.bot.user.avatar_url)
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed.description = f"\nUse **!ticket <ticketpanelname>**"
        else:
            embed.description = f"\nYou don't have permissions for executing this command."

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.check(check_if_has_permission)
    async def add(self, ctx, member: Member):
        """Create ticket for mentioned mamber

        Args:
            ctx ([type]): [description]
            member (Member): owner of the ticket
        """
        await self.create_ticket(member,ctx.guild)
        embed : Embed = settings.get_ticket_panel_embed()
        embed.description = 'Ticket created with success!'
        embed.set_footer(text=embed.footer.text, icon_url=self.bot.user.avatar_url)
        await ctx.message.delete()
        await ctx.send(embed=embed)

    @add.error
    async def add_error(self, ctx, error):
        """ Handles errors caused in the add command 
        """
        embed: Embed = settings.get_ticket_error_embed()

        embed.set_footer(text=embed.footer.text,
                         icon_url=self.bot.user.avatar_url)
        print(error)
        if isinstance(error, commands.MissingRequiredArgument):
            embed.description = f"\nUse **!add <user>**"
        elif isinstance(error, commands.BadArgument):
            embed.description = f"\nUser not found."
        else:
            embed.description = f"\nYou don't have permissions for executing this command."

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    @commands.check(check_if_is_ticket)
    async def close(self, ctx):
        """Command for closing the ticket

        Args:
            ctx ([type]): [description]
        """
        await self.close_ticket(ctx.channel)

    @close.error
    async def close_error(self, ctx, error):
        """ Handles errors caused in the add command 
        """
        embed: Embed = settings.get_ticket_error_embed()

        embed.set_footer(text=embed.footer.text,
                         icon_url=self.bot.user.avatar_url)

        embed.description = f"\nYou must be inside a **ticket** to execute this command."

        await ctx.send(embed=embed)

    async def create_ticket(self, member : Member, guild : Guild):
        """Creates ticket for given member and guild

        Args:
            member (Member): The member owner of the ticket
            guild (Guild): The guild where the ticket will be created
        """
        licence_id = await servers.get_licence_id(guild.id)
        category : CategoryChannel = guild.get_channel(await self.categorys.get_category_id(licence_id))
        role = guild.get_role(await self.roles.get_role_id(licence_id))
        

        channel : TextChannel = await category.create_text_channel(f'ticket-{member.name}')

        overwrite_everyone = PermissionOverwrite()
        overwrite_everyone.send_messages = False
        overwrite_everyone.read_messages = False

        overwrite_member = PermissionOverwrite()
        overwrite_member.send_messages = True
        overwrite_member.read_messages = True


        everyone_role = guild.default_role

        await channel.set_permissions(target=everyone_role,overwrite=overwrite_everyone)
        await channel.set_permissions(target=member, overwrite=overwrite_everyone)
        await channel.set_permissions(target=role, overwrite=overwrite_member)
        await channel.send(content = member.mention + " " + role.mention)
    
    async def close_ticket(self, channel : TextChannel):
        """Deletes ticket

        Args:
            channel (TextChannel): Ticket channel who will be closed
        """
        await channel.delete()

    async def reload_cog(self, licence_id: int):
        await self.categorys.update_category_id(licence_id)
        await self.roles.update_role_id(licence_id)
