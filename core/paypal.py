from os import name
from typing import Coroutine
from aiohttp import ClientSession, BasicAuth
from datetime import datetime, timedelta
from base64 import standard_b64encode
from modules.base import Base
from discord.ext import commands
import functools


class AccessToken():

    def __init__(self, token: str, expires_in: int):
        self.token: str = token
        self.valid_until = datetime.utcnow() + timedelta(seconds=expires_in)

    def has_expired(self) -> bool:
        return self.valid_until < datetime.utcnow()


class Product():

    def __init__(self, id: str, name: str, description: str, product_type: str, category: str, image_url: str, home_url: str):
        self.id = id
        self.name = name
        self.description = description
        self.type = product_type
        self.category = category
        self.image_url = image_url
        self.home_url = home_url


class Paypal(ClientSession):

    def __init__(self, client_id: str, secret: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {'Content-Type': 'application/json',
                        'Accept-Language': 'en_US', 'Accept': 'application/json'}
        self.client_id = client_id
        self.secret = secret
        self.access_token: AccessToken

    async def auth(self) -> AccessToken:

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'client_credentials'
        }

        response = await self.post(url='https://api-m.sandbox.paypal.com/v1/oauth2/token', auth=BasicAuth(login=self.client_id, password=self.secret), data=data, headers=headers)

        response_data = await response.json()

        if response_data.get('error'):
            raise Exception('Invalid credentials on paypal')
            return None

        return AccessToken(response_data.get('access_token'), response_data.get('expires_in'))

    def middleware_authentification(self,func):
        @functools.wraps(func)
        async def wrapper(self, *args, **kwargs):
            if not self.access_token or self.access_token.has_expired():
                self.access_token = await self.auth()
            return await func(self, *args, **kwargs)
        return wrapper

    @middleware_authentification(func=create_pro)
    async def create_product(self) -> Product:
        payload = {
            'name': 'Ark Consoles Server Manager Bot',
            'description': 'Discord bot',
            'type': 'SERVICE',
            'category': 'SOFTWARE',
            'image_url': 'https://www.tipsandtricks-hq.com/wp-content/uploads/2013/08/paypal-custom-page-style-example-screenshot.png',
            'home_url': 'https://discord.bot'
        }

        response = await self.post(url='https://api-m.sandbox.paypal.com/v1/catalogs/products', data=payload)
        print(await response.json())
        return None

    @middleware_authentification
    async def create_plan(self, product_id: string, name: string, billing_cycles[])


paypal = Paypal(client_id='AQe1TviDM0qgWN9jjBkrFBYrrZoGVrx-1B_6XfMhIHwG245MwRqA4Wt1NIxgrfALXKgMw55r9qI5pw8Z',
                secret='EKzz7v1XX538khOZQvUcmJh7s3P91BWL0wC98nINx8xqB1A0p0xmKT3xly8CkSrU_qvUP-1ZUhVMzcNq')


class PaypalCog(Base):

    @commands.Cog.listener()
    async def on_connect(self):
        await paypal.auth()
