from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed, Guild, Member, Role, Permissions
from models.module import Module
from core.role import Roles
from core.servers import servers
from models.role import Role as RoleORM


class LowHierarchyError(commands.UserInputError):

    def __init__(self, author, target, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author
        self.target = target


class Moderation(Base):



    @commands.Cog.listener()
    async def on_ready(self):
        role_name = "Moderation Role"
        module = await Module.query.where(Module.name == 'Moderation').gino.first()

        if not module:
            module = await Module.create(name = 'Moderation')

        role = await RoleORM.query.where(RoleORM.name == role_name).where(RoleORM.module_id == module.id).gino.first()
        if not role:
            role = await RoleORM.create(name=role_name, module_id=module.id)

        role_id = role.id
        self.roles: Roles = Roles(
            role_id=role_id, default_id=784514780554985572)

    async def check_if_has_permission(ctx):
        """Check if user has permission for command
        """
        licence_id = await servers.get_licence_id(ctx.guild.id)
        role_id = await ctx.command.cog.roles.get_role_id(licence_id)
        author = ctx.author
        role = ctx.guild.get_role(role_id)
        return role in author.roles

    def check_hierachy(self, author: Member, target: Member):
        """Check if author has higher hierachy then the target

        """
        if author.roles[-1] < target.roles[-1]:
            raise LowHierarchyError(author, target)

    """
        Command mute, mute player
    """
    @commands.command(pass_context=True, usage="-mute <member>")
    @commands.check(check_if_has_permission)
    async def mute(self, ctx, target: Member):
        self.check_hierachy(author=ctx.author, target=target)
        await target.add_roles(await self.get_muted_role(ctx.guild))
        embed = settings.get_moderation_core_embed()
        embed.description = f"Member **{target.name}** muted."
        await ctx.send(embed=embed)

    """
        Command unmute, unmute player
    """
    @commands.command(pass_context=True, usage="-unmute <member>")
    @commands.check(check_if_has_permission)
    async def unmute(self, ctx, target: Member):
        self.check_hierachy(author=ctx.author, target=target)
        await target.remove_roles(await self.get_muted_role(ctx.guild))
        embed = settings.get_moderation_core_embed()
        embed.description = f"Member **{target.name}** unmuted."
        await ctx.send(embed=embed)

    """
        Command ban, ban player
    """
    @commands.command(pass_context=True, usage="-ban <member>")
    @commands.check(check_if_has_permission)
    async def ban(self, ctx, target: Member):
        self.check_hierachy(author=ctx.author, target=target)
        await target.ban()
        embed = settings.get_moderation_core_embed()
        embed.description = f"Member **{target.name}** banned."
        await ctx.send(embed=embed)

    """
        Command unban, unban player
    """
    @commands.command(pass_context=True, usage="-unban <member>")
    @commands.check(check_if_has_permission)
    async def unban(self, ctx, target_str: str):
        guild: Guild = ctx.guild
        embed = settings.get_moderation_core_embed()
        target: Member = None
        print(await guild.bans())
        for reason, user in await guild.bans():
            print(user)
            if user.name in target_str:
                target = user
                break
            
            try:
                if user.id == int(target_str):
                    target = user
                    break
            except:
                pass

        if not target:
            embed.description = "User not found."
            await ctx.send(embed=embed)
            return

        await ctx.guild.unban(target)
        embed.description = f"Member **{target.name}** unbanned."
        await ctx.send(embed=embed)

    """
        Command kick, kick player
    """
    @commands.command(pass_context=True, usage="-kick <member>")
    @commands.check(check_if_has_permission)
    async def kick(self, ctx, target: Member):
        self.check_hierachy(author=ctx.author, target=target)
        await target.kick()
        embed = settings.get_moderation_core_embed()
        embed.description = f"Member **{target.name}** kicked."
        await ctx.send(embed=embed)

    """
        Command clear, clear last x messages from chat
    """
    @commands.command(pass_context=True, usage="-clear <number of lines>")
    @commands.check(check_if_has_permission)
    async def clear(self, ctx, number_of_messages: int):
        await ctx.channel.purge(limit=number_of_messages)
        embed = settings.get_moderation_core_embed()
        embed.description = f"Last {number_of_messages} messages deleted."
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        author: Member = message.author
        if await self.get_muted_role(message.guild) in author.roles:
            await message.delete()

    @mute.error
    @unmute.error
    @ban.error
    @unban.error
    @kick.error
    @clear.error
    async def on_error(self, ctx, error):
        """Handles the errors from the commands

        Args:
            ctx ([type]): [description]
            error ([type]): [description]
        """
        print(type(error))
        if isinstance(error, LowHierarchyError):
            embed = settings.get_moderation_core_embed()
            embed.set_footer(text=embed.footer.text,
                             icon_url=self.bot.user.avatar_url)
            embed.description = f"**{error.target.name}** has a higher role than yours."

            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MemberNotFound):
            embed = settings.get_moderation_core_embed()
            embed.set_footer(text=embed.footer.text,
                             icon_url=self.bot.user.avatar_url)
            embed.description = f"Player not found."
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            embed = settings.get_moderation_core_embed()
            embed.set_footer(text=embed.footer.text,
                             icon_url=self.bot.user.avatar_url)
            embed.description = f"Wrong syntax, try **{ctx.command.usage}**"
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CheckFailure):
            embed = settings.get_moderation_core_embed()
            embed.set_footer(text=embed.footer.text,
                             icon_url=self.bot.user.avatar_url)
            embed.description = f"You don't have permission to use this command."
            await ctx.send(embed=embed)

    async def get_muted_role(self, guild: Guild) -> Role:
        for role in guild.roles:
            if role.name == "muted-role":
                return role

        permissions = Permissions()
        permissions.send_messages = False
        role = await guild.create_role(name='muted-role', permissions=permissions)

    async def reload_cog(self, licence_id: int):
        await self.roles.update_role_id(licence_id)
