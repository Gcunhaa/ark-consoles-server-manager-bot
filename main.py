from core.database import DatabaseCog
from discord.ext.commands import Bot
from core import settings
from core.database import DatabaseCog
from core.redis import RedisCog


#from core.paypal import PaypalCog

#Create and configurate the client bot
bot = Bot(
    command_prefix= settings.get_command_prefix()
)


#Event run when bot start
@bot.event
async def on_ready():
    print('\n\n---- BOT STARTED ----')
    print(f'Bot name: {bot.user.name}')
    print(f'Bot id: {bot.user.id}')
    print('---------------------')


bot.add_cog(DatabaseCog(bot))
bot.add_cog(RedisCog(bot))

from modules.licence import Licence
from modules.ticket import Ticket
from modules.reload import Reload
from modules.flip import Flip
from modules.numbergen import Numbergen
from modules.timezone import Timezone
from modules.suggestion import Suggestion
from modules.slap import Slap
from modules.moderation import Moderation
from modules.economy import Economy

bot.add_cog(Licence(bot))
bot.add_cog(Ticket(bot))
bot.add_cog(Reload(bot))
bot.add_cog(Flip(bot))
bot.add_cog(Numbergen(bot))
bot.add_cog(Timezone(bot))
bot.add_cog(Suggestion(bot))
bot.add_cog(Slap(bot))
bot.add_cog(Moderation(bot))
bot.add_cog(Economy(bot))
#bot.add_cog(PaypalCog(bot))

if __name__ == '__main__':
    #Run the bot
    bot.run(settings.get_bot_token())