from discord.ext.commands import Bot
from core import settings
from modules.suggestion import Suggestion
from modules.links import Links
from modules.ticket import Ticket

#Create and configurate the client bot
bot = Bot(
    command_prefix= settings.get_command_prefix()
)



#Event run when bot start
@bot.event
async def on_ready():
    print('---- BOT STARTED ----')
    print(f'Bot name: {bot.user.name}')
    print(f'Bot id: {bot.user.id}')
    print('---------------------')

bot.add_cog(Suggestion(bot))
bot.add_cog(Links(bot))
bot.add_cog(Ticket(bot))

if __name__ == '__main__':
    #Run the bot
    bot.run(settings.get_bot_token())