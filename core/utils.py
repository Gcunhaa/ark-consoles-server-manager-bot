from models import licence
from aioredis import Redis
from gino import Gino
from discord.ext.commands import Bot, check
from typing import Optional
from .servers import servers

def next_page(licences : list, limit : int, skip: int) -> list:
    last = skip + limit
    if len(licences) < skip or len(licences) < last:
        last = len(licences)

    return licences[skip:last]

async def check_if_has_permission(f):

        async def predicate(*args):
            print(args)
            self = args[0]
            ctx = args[1]
            #licence_id = await servers.get_licence_id(ctx.guild.id)
            #role = await self.roles.get_role_id(licence_id)
            print(ctx.author)
            #print(role)
            #print(licence_id)
            return True

        return check(await predicate)