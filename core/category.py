from models.category import Category
from models.licence import Licence
from models.licence_category import LicenceCategory
from typing import Any, Union


class Categorys():

    def __init__(self, category_id: int, default_id: int):
        # Licence Id : Server Id
        self.categorys = {}
        self.category_id = category_id
        self.default_id = default_id

    async def get_category_id(self, licence_id: int) -> Union[Any, int]:
        """Retrieves the category id

        Args:
            licence_id (int): the licence id

        Returns:
            int: server id
        """

        if not self.categorys.get(licence_id):
            await self.update_category_id(licence_id)

        category_id = self.categorys.get(licence_id)

        return category_id

    async def update_category_id(self, licence_id: int):
        """[Updates the server id of given licence_ice]

        Args:
            licence_id (int): the licence id

        Raises:
            Exception: License id has no server
        """
        category: LicenceCategory = await LicenceCategory.query.where(LicenceCategory.licence_id == licence_id).where(LicenceCategory.category_id == self.category_id).gino.first()

        if not category:
            licence: Licence = await Licence.get(licence_id)
            if not licence:
                raise Exception(
                    f'License id doesnt exist - Category {self.category_id}')
            else:
                category: LicenceCategory = await LicenceCategory.create(licence_id=licence_id, category_id=self.category_id, category_discord_id=self.default_id)

        self.categorys.update({licence_id: category.category_discord_id})