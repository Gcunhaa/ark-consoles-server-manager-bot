from models.category import Category
from models.licence import Licence
from models.licence_channel import LicenceChannel
from typing import Any, Union


class Channels():

    def __init__(self, channel_id: int, default_id: int):
        # Licence Id : Server Id
        self.channels = {}
        self.channel_id = channel_id
        self.default_id = default_id

    async def get_channel_id(self, licence_id: int) -> Union[Any, int]:
        """Retrieves the category id

        Args:
            licence_id (int): the licence id

        Returns:
            int: server id
        """

        if not self.channels.get(licence_id):
            await self.update_channel_id(licence_id)

        channel_id = self.channels.get(licence_id)

        return channel_id

    async def update_channel_id(self, licence_id: int):
        """[Updates the server id of given licence_ice]

        Args:
            licence_id (int): the licence id

        Raises:
            Exception: License id has no server
        """
        channel: LicenceChannel = await LicenceChannel.query.where(LicenceChannel.licence_id == licence_id).where(LicenceChannel.channel_id == self.channel_id).gino.first()

        if not channel:
            licence: Licence = await Licence.get(licence_id)
            if not licence:
                raise Exception(
                    f'License id doesnt exist - Category {self.channel_id}')
            else:
                channel: LicenceChannel = await LicenceChannel.create(licence_id=licence_id, channel_id=self.channel_id, channel_discord_id=self.default_id)

        self.channels.update({licence_id: channel.channel_discord_id})
