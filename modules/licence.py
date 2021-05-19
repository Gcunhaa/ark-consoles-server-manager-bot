from .base import Base
from discord import Member
from discord.ext import commands
from core import settings
from discord import Embed, Member, TextChannel
from core.utils import next_page
from typing import TYPE_CHECKING, Text
import asyncio
from secrets import token_urlsafe
from models.licence import Licence as LicenceORM
from models.server import Server as ServerORM
from core.redis import redis

class Licence(Base):

    """
        Command licence, return licence manager embed
    """

    @commands.command()
    async def licence(self, ctx):
        """Licence command
        """
        await self.licences_info(member=ctx.author, channel=ctx.channel)

    async def licences_info(self, member: Member, channel: TextChannel):
        """Show all licences from user, if has none asks if wants to create it

        """
        licences = await LicenceORM.query.where(LicenceORM.user_discord_id == member.id).gino.all()
        if len(licences) == 0:
            await self.show_no_licences_embed(member=member, channel=channel)
            return

        # Show licences
        message = await channel.send(content="Loading info...")
        await self.show_licences(licences=licences, member=member, message=message)

    async def show_no_licences_embed(self, member: Member, channel: TextChannel):
        """Show the embed to create licence and create if user reacts.

        Args:
            member (Member): Member that has no licence 
            channel (TextChannel): Channel to send the embed

        """
        embed: Embed = settings.get_licence_no_licence_embed()
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=embed.footer.text,
                         icon_url=self.bot.user.avatar_url)

        message = await channel.send(embed=embed, content=member.mention)
        await message.add_reaction(emoji=settings.get_licence_new_licence_emoji())

        def check_reaction(reaction, author):
            return author == member and reaction.message == message and reaction.emoji == settings.get_licence_new_licence_emoji()

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await message.clear_reactions()
            await self.create_licence(member)

        except asyncio.TimeoutError:
            embed.description = "**Process stopped**.\nYou took to long to reply, please try again."
            await message.edit(embed=embed)
            await message.clear_reactions()
        else:
            embed.title = 'Success!'
            embed.description = 'Licence created with success.\nPlease proceed to **payment** instructions in DM.'
            await message.edit(embed=embed)

    async def show_licences(self, licences: list, member, message, limit: int = 5, skip: int = 0):
        """Show multiple licences from the user

        Args:
            member (Member): owner of the licences
            limit (int, optional): How many licences to print. Defaults to 5.
            skip (int, optional): How many licences to skip. Defaults to 0.
        """
        embed: Embed = settings.get_licence_show_licences_embed()
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=embed.footer.text,
                         icon_url=self.bot.user.avatar_url)

        selection_emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

        event_emojis = []

        current_page = next_page(licences, limit, skip)

        n = 0
        for licence in current_page:
            embed.description = embed.description + \
                f"\n{selection_emojis[n]}| {licence.id} | {licence.is_active} "
            n = n + 1

        await message.edit(embed=embed, content=member.mention)

        if(skip >= limit):
            await message.add_reaction('⏪')
            event_emojis.append('⏪')

        for emoji in selection_emojis[:n]:
            await message.add_reaction(emoji)

        next = next_page(licences=licences, limit=limit, skip=skip+limit)
        if len(next) > 0:
            await message.add_reaction('⏩')
            event_emojis.append('⏩')

        await message.add_reaction(settings.get_licence_new_licence_emoji())
        event_emojis.append(settings.get_licence_new_licence_emoji())

        event_emojis = event_emojis + selection_emojis[:n]

        def check_reaction(reaction, author):
            return author == member and reaction.message == message and reaction.emoji in event_emojis

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await message.clear_reactions()

            if reaction.emoji == '⏩':
                await self.show_licences(licences=licences, member=member, message=message, skip=skip+limit)
                return
            if reaction.emoji == '⏪':
                await self.show_licences(licences=licences, member=member, message=message, skip=skip-limit)
                return
            if reaction.emoji == settings.get_licence_new_licence_emoji():
                await self.create_licence(member=member)
                embed.title = 'Success!'
                embed.description = 'Licence created with success.\nPlease proceed to **payment** instructions in DM.'
                await message.edit(embed=embed)
                await message.clear_reactions()
                
                return
            if reaction.emoji in selection_emojis[:n]:
                index = selection_emojis.index(reaction.emoji)

                await self.show_licence(member=member, licence=current_page[index], message=message, embed=embed)
                return
        except asyncio.TimeoutError:
            embed.description = "**Process stopped**.\nYou took to long to reply, please try again."
            await message.edit(embed=embed)
            await message.clear_reactions()

    async def show_licence(self, member: Member, licence : LicenceORM, message, embed : Embed):
        """Shows licence info about given licence

        Args:
            member (Member): owner of the licence
            licence (LicenceORM): licence that info will be showed off
            message: the message that will bee updated
            embed: the embed that will be updated
        """
        embed.description = ''
        reaction_options = ['💳']

        if licence.is_active:
            await message.add_reaction('⚙️')
            embed.description = f"\nTo edit this licence  ⚙️"
            reaction_options.append('⚙️')
        embed.description = embed.description + '\nTo resend payment link  💳\n\n'

        

        embed.add_field(name='Licence ID',value=f'```{licence.id} ```', inline=True)
        embed.add_field(name='Active',value=f'```{licence.is_active} ```', inline=True)
        embed.add_field(name='Server ID',value=f'```784045696524615700 ```', inline=False)
        embed.add_field(name='Payment Status',value=f'```Pending... ```', inline=True)
        await message.edit(embed=embed)

        
        await message.add_reaction('💳')
        

        def check_reaction(reaction, author):
            return author == member and reaction.message == message and reaction.emoji in reaction_options

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
            await message.clear_reactions()

            if reaction.emoji == '⚙️':
                embed.description = 'Link for managing the licence sent to your DM'
                embed.clear_fields()
                await self.send_licence_dashboard_url(licence=licence, member=member)
                await message.edit(embed=embed)
                return
        except asyncio.TimeoutError:
            embed.description = "**Process stopped**.\nYou took to long to reply, please try again."
            await message.edit(embed=embed)
            await message.clear_reactions()
            
    async def create_licence(self, member: Member):
        """Create licence for user

        Args:
            member (Member): member owner of the licence
        """
        # TODO: Enviar dm para pagamento
        licence = await LicenceORM.create(user_discord_id=member.id)
        await ServerORM.create(licence_id = licence.id, server_discord_id=784514443479351346)
        for cog in self.bot.cogs:
            await self.bot.get_cog(cog).reload_cog(licence.id)

    async def send_licence_dashboard_url(self, licence : LicenceORM, member: Member):
        """sends the url for managing the licence in DM

        Args:
            licence (LicenceORM): licence that will have the url generated
            member (Member): user who will receive the dashboard link
        """
        url = await self.generate_licence_dashboard_url(licence=licence)
        embed = settings.get_licence_show_licences_embed()
        embed.set_footer(text=embed.footer.text, icon_url=self.bot.user.avatar_url)
        embed.description = f'The url for managing your licence is {url}\nThis url will expire in 60 minutes.\n\n**Do not share this link if anyone by any chance**'
        await member.send(embed=embed)

    async def generate_licence_dashboard_url(self, licence: LicenceORM) -> str:
        """Generate url for managing the licence

        Args:
            licence (LicenceORM): licence that will have the dashboard generated

        Returns:
            str: url of dashboard
        """
        token = token_urlsafe(6)
        await redis.conn.psetex(token,60*1000*60, str(licence.id))
        return settings.get_dashboard_endpoint() + token