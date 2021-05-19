from modules.base import Base
from discord.ext import commands
from core import settings
from aioredis import Redis, create_redis_pool


class RedisClass():
    
    async def start(self):
        self.conn : Redis = await create_redis_pool(address=settings.get_redis_hostname(), password=settings.get_redis_password())

    async def close(self):
        await self.conn.wait_closed()
    
redis = RedisClass()

class RedisCog(Base):
    """
        Create redis pool
    """
    @commands.Cog.listener()
    async def on_connect(self):
        print('[!] Connecting to the REDIS server')
        try:
            await redis.start()
        except Exception as exception:
            print('[-] Failed to connect to REDIS server')
            print(exception)
            print('----- BOT SHUTDOWN -----')
            await self.bot.close()
            return
        
        print('[+] Connected to the REDIS server with success')
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        print('[!] Disconnecting from the REDIS server')
        await redis.close()