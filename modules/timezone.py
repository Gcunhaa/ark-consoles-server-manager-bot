from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed
from datetime import date, datetime
from pytz import timezone


class Timezone(Base):

    """
        Command timezone, show time based on timezone
    """
    @commands.command()
    async def timezone(self, ctx, timezone_name: str):

        embed = Embed()
        embed.set_footer(text='Ark Consoles Server Manager',
                         icon_url=self.bot.user.avatar_url)

        try:
            tz = timezone(timezone_name)
        
            time = datetime.now(tz)
            #TODO: Add to config timezone to nick(PST : America/Los_Angeles)
            embed.description = f"Today is {time.strftime('%A')} in {tz.zone}, and the time is {time.hour}:{time.minute}"
        except:
            embed.description = f"Timezone : **{timezone_name}** not found."

        await ctx.send(embed=embed)
