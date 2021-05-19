from models.role import Role
from models.licence import Licence
from models.licence_role import LicenceRole
from typing import Any, Union


class Roles():

    def __init__(self, role_id: int, default_id: int):
        # Licence Id : Role id
        self.roles = {}
        self.role_id = role_id
        self.default_id = default_id

    async def get_role_id(self, licence_id: int) -> Union[Any, int]:
        """Retrieves the role id

        Args:
            licence_id (int): the licence id

        Returns:
            int: server id
        """

        if not self.roles.get(licence_id):
            await self.update_role_id(licence_id)

        role_id = self.roles.get(licence_id)

        return role_id

    async def update_role_id(self, licence_id: int):
        """[Updates the role id of given licence_ice]

        Args:
            licence_id (int): the licence id

        Raises:
            Exception: License id has no server
        """
        role : LicenceRole = await LicenceRole.query.where(LicenceRole.licence_id == licence_id).where(LicenceRole.role_id == self.role_id).gino.first()

        if not role:
            licence: Licence = await Licence.get(licence_id)
            if not licence:
                raise Exception(
                    f'Role id doesnt exist - Role {self.role_id}')
            else:
                role: LicenceRole = await LicenceRole.create(licence_id=licence_id, role_id=self.role_id, role_discord_id=self.default_id)

        self.roles.update({licence_id: role.role_discord_id})
