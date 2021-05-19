from models.server import Server
from typing import Any, Union


class Servers():

    def __init__(self):
        # Server ID : Licence ID
        self.servers = {}

    async def update_server_id(self, licence_id: int):
        """[Updates the server id of given licence_ice]

        Args:
            licence_id (int): the licence id

        Raises:
            Exception: License id has no server
        """

        server: Server = await Server.query.where(Server.licence_id == licence_id).gino.first()

        if not server:
            raise Exception('Licence id has no server')

        self.servers.update({server.server_discord_id : server.licence_id})

    async def get_licence_id(self, server_id : int) -> Union[Any, int]:
        """Retrevies the licence id of given id

        Args:
            server_id (int): id of the server

        """

        if not self.servers.get(server_id):
            server = await Server.query.where(Server.server_discord_id == server_id).gino.first()
            if not server:
                raise Exception('Server has no licence attached')
            await self.update_server_id(server.licence_id)

        licence_id = self.servers.get(server_id)
        return licence_id

        


    async def get_server_id(self, licence_id: int) -> Union[Any, int]:
        """Retrieves the server id

        Args:
            licence_id (int): the licence id

        Returns:
            int: server id
        """

        for k,v in self.servers.items():
            if v == licence_id:
                return k
        
        return await self.update_server_id(licence_id)

    


servers = Servers()
