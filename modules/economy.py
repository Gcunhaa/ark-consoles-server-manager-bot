from .base import Base
from discord.ext import commands
from core import settings
from discord import Embed, Guild
from models.module import Module
from core.channel import Channels
from core.servers import servers
from models.setting import Setting
from models.economy import Economy as EconomyORM
from core.setting import Settings


class PositiveInt(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            n = int(argument)
            if n <= 0:
                raise Exception()
            return n
        except:
            raise commands.ArgumentParsingError()

class Economy(Base):

    @commands.Cog.listener()
    async def on_ready(self):
        module_name = 'Economy'
        interest_name = "Interest rate"
        interest_time_name = "Interest time"
        rob_amount_name = "Rob amount"
        module = await Module.query.where(Module.name == module_name).gino.first()

        if not module:
            module = await Module.create(name=module_name)

        setting_interest = await Setting.query.where(Setting.name == interest_name).where(Setting.module_id == module.id).gino.first()
        if not setting_interest:
            setting_interest = await Setting.create(name=interest_name, module_id=module.id)

        setting_interest_time = await Setting.query.where(Setting.name == interest_time_name).where(Setting.module_id == module.id).gino.first()
        if not setting_interest_time:
            setting_interest_time = await Setting.create(name=interest_time_name, module_id=module.id)

        setting_rob = await Setting.query.where(Setting.name == rob_amount_name).where(Setting.module_id == module.id).gino.first()
        if not setting_rob:
            setting_rob = await Setting.create(name=rob_amount_name, module_id=module.id)

        self.settings_interest_time = Settings(setting_interest_time.id, "5")
        self.settings_interest = Settings(setting_interest.id, "10")
        self.settings_rob_amount = Settings(setting_rob.id, "200")
        await servers.get_server_id(10)

    @commands.command()
    async def bal(self, ctx):
        """ bal command, shows balance of currency in wallet and bank
        """
        embed: Embed = Embed()
        embed.description = f"{ctx.author.mention} balance is\n\n**Wallet**: {await self.get_wallet_balance(ctx.author.id,ctx.guild.id)}\n**Bank**: {await self.get_bank_balance(ctx.author.id,ctx.guild.id)}"
        await ctx.send(embed=embed)

    @commands.command()
    async def deposit(self, ctx, amount: PositiveInt):
        """ deposit command, transfer amount from the wallet to the bank
        """
        await self.economy_deposit(amount=amount, user_discord_id=ctx.author.id, server_id=ctx.guild.id)
        embed: Embed = Embed()
        embed.description = f"Success! **{amount}** was transferred from your wallet to your bank account"
        await ctx.send(embed=embed)

    @commands.command()
    async def withdraw(self, ctx, amount: PositiveInt):
        """ withdraw command, transfer amount from the bank to the wallet
        """
        await self.economy_withdraw(amount=amount, user_discord_id=ctx.author.id, server_id=ctx.guild.id)
        embed: Embed = Embed()
        embed.description = f"Success! **{amount}** was transferred from your bank account to your wallet"
        await ctx.send(embed=embed)

    @bal.error
    @deposit.error
    @withdraw.error
    async def on_error(self, ctx, error):
        """ Handles errors from the commands"""
        embed = Embed()
        print(type(error))
        if isinstance(error, NotSufficientFund):
            embed.description = "There is no sufficient funds for executing this operation."
            await ctx.send(embed=embed)

    async def get_bank_balance(self, user_discord_id: int, server_id: int):
        """Responsible for retrieving the amount in the bank

        Args:
            user_discord_id (int): user discord id that want to get the balance checked
            server_id (int): server discord id that the user is in
        """
        economy: EconomyORM = await EconomyORM.query.where(EconomyORM.licence_id == servers.get_licence_id(server_id)).where(EconomyORM.user_discord_id == user_discord_id).gino.first()
        if not economy:
            return 0
        return economy.bank

    async def get_wallet_balance(self, user_discord_id: int, server_id: int):
        """Responsible for retrieving the amount in the wallet

        Args:
            user_discord_id (int): user discord id that want to get the balance checked
            server_id (int): server discord id that the user is in
        """
        economy: EconomyORM = await EconomyORM.query.where(EconomyORM.licence_id == servers.get_licence_id(server_id)).where(EconomyORM.user_discord_id == user_discord_id).gino.first()
        if not economy:
            return 0
        return economy.wallet

    async def economy_deposit(self, amount: int, user_discord_id: int, server_id: int):
        """Responsible for depositing the amount in the wallet

        Args:
            amount (int): amount that will be transfered from the wallet to the bank
            user_discord_id (int): user discord id that is operating
            server_id (int): server discord id that the user is in
        """
        economy: EconomyORM = await EconomyORM.query.where(EconomyORM.licence_id == servers.get_licence_id(server_id)).where(EconomyORM.user_discord_id == user_discord_id).gino.first()
        if not economy or economy.wallet < amount:
            raise NotSufficientFund()

        bank_bal = economy.bank + amount
        wallet_bal = economy.wallet - amount
        await economy.update(bank=bank_bal, wallet=wallet_bal).apply()

    async def economy_withdraw(self, amount: int, user_discord_id: int, server_id: int):
        """Responsible for withdrawing the amount in the bank

        Args:
            amount (int): amount that will be transfered from the wallet to the bank
            user_discord_id (int): user discord id that is operating
            server_id (int): server discord id that the user is in
        """
        economy: EconomyORM = await EconomyORM.query.where(EconomyORM.licence_id == servers.get_licence_id(server_id)).where(EconomyORM.user_discord_id == user_discord_id).gino.first()
        if not economy or economy.bank < amount:
            raise NotSufficientFund()

        bank_bal = economy.bank - amount
        wallet_bal = economy.wallet + amount
        await economy.update(bank=bank_bal, wallet=wallet_bal).apply()

    async def economy_add(self, amount: int, user_discord_id: int, server_id: int):
        """Responsible for adding the amount in the wallet

        Args:
            amount (int): amount that will be transfered from the wallet to the bank
            user_discord_id (int): user discord id that is operating
            server_id (int): server discord id that the user is in
        """
        if amount < 1:
            raise Exception('added amount can not be negative or 0')
        economy : EconomyORM = await self.economy_get_or_create(user_discord_id=user_discord_id,server_id=server_id)
        wallet_bal = economy.wallet + amount
        await economy.update(wallet=wallet_bal).apply()

    async def economy_remove(self, amount: int, user_discord_id: int, server_id: int):
        """Responsible for removing the amount in the wallet

        Args:
            amount (int): amount that will be transfered from the wallet to the bank
            user_discord_id (int): user discord id that is operating
            server_id (int): server discord id that the user is in
        """
        if amount < 1:
            raise Exception('removed amount can not be negative or 0')
        economy : EconomyORM = await self.economy_get_or_create(user_discord_id=user_discord_id,server_id=server_id)
        if economy.wallet < amount:
            amount = economy.wallet
        wallet_bal = economy.wallet - amount
        await economy.update(wallet=wallet_bal).apply()

    async def economy_get_or_create(self, user_discord_id: int, server_id: int) -> EconomyORM:
        economy: EconomyORM = await EconomyORM.query.where(EconomyORM.licence_id == servers.get_licence_id(server_id)).where(EconomyORM.user_discord_id == user_discord_id).gino.first()
        if not economy:
            economy = await EconomyORM.create(user_discord_id=user_discord_id,licence_id=servers.get_licence_id(server_id=server_id))
        return economy

    async def reload_cog(self, licence_id: int):
        await self.settings_interest.update_setting_value(licence_id)
        await self.settings_rob_amount.update_setting_value(licence_id)
        await self.settings_interest_time.update_setting_value(licence_id)


class NotSufficientFund(commands.CommandError):
    pass
