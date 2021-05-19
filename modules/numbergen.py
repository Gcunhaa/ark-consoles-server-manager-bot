from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed
from random import randint
from models.module import Module
from models.setting import Setting
from core.setting import Settings
from core.servers import servers

class Numbergen(Base):

    @commands.Cog.listener()
    async def on_ready(self):
        module_name = 'Number Gen'
        min_name = "Min Number"
        max_name = "Max Number"
        module = await Module.query.where(Module.name == module_name).gino.first()

        if not module:
            module = await Module.create(name=module_name)

        
        setting_min = await Setting.query.where(Setting.name == min_name).where(Setting.module_id == module.id).gino.first()
        if not setting_min:
            setting_min = await Setting.create(name=min_name, module_id=module.id)
            

        setting_max = await Setting.query.where(Setting.name == max_name).where(Setting.module_id == module.id).gino.first()
        if not setting_max:
            setting_max = await Setting.create(name=max_name, module_id=module.id)

        
        self.min_settings = Settings(setting_min.id,default_value=str(0))
        self.max_settings = Settings(setting_max.id,default_value=str(100))
        await servers.get_server_id(10)

    """
        Command numbergen, generates random number based on the min and max range from the settings 
    """
    @commands.command()
    async def numbergen(self, ctx):
        licence_id = await servers.get_licence_id(ctx.guild.id)
        min = int(await self.min_settings.get_setting_value(licence_id))
        max = int(await self.max_settings.get_setting_value(licence_id))
        num = randint(min, max)
        embed = Embed()
        embed.set_footer(text='Ark Consoles Server Manager', icon_url=self.bot.user.avatar_url)
        embed.description = f"You generated a number from {min} to {max}.\nNumber: **{num}**"

        await ctx.send(embed=embed)

    async def reload_cog(self, licence_id: int):
        await self.min_settings.update_setting_value(licence_id)
        await self.max_settings.update_setting_value(licence_id)