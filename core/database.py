from modules.base import Base
from discord.ext import commands
from core import settings
from discord import Embed
from gino import Gino

class Database():
    
    def __init__(self):
       self.db = Gino()
    
    async def start(self):
        await self.db.set_bind(settings.get_postgres_dsn())
    
    async def close(self):
        await self.db.pop_bind().close()
    
database = Database()

class DatabaseCog(Base):


    """
        Bind to the server
    """
    @commands.Cog.listener()
    async def on_connect(self):
        print('\n[!] Connecting to the PGSQL server')
        try:
            await database.start()
        except Exception as exception:
            print('[-] Failed to connect to PGSQL server')
            print(exception)
            print('----- BOT SHUTDOWN -----')
            return
        
        print('[+] Connected to the PGSQL server with success')

    @commands.Cog.listener()
    async def on_disconnect(self):
        print('[!] Disconnecting from the PGSQL server')
        await database.close()