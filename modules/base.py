from discord.ext.commands import Bot
from discord.ext import commands

"""[summary]
  Base class for modules implementation
  
  Parameters:
  bot: The client instance of the bot
  name: the name that is going to be used for the command
"""
class Base(commands.Cog):

    def __init__(self, bot : Bot):
        self.load_module_event()
        self.bot = bot
 
    """[summary]

        Method called when module is initialized

    """
    def load_module_event(self):
        pass
