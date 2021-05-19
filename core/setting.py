from models.category import Category
from models.licence import Licence
from models.licence_setting import LicenceSetting
from typing import Any, Union


class Settings():

    def __init__(self, setting_id: int, default_value: str):
        # Licence Id : Value
        self.settings = {}
        self.setting_id = setting_id
        self.default_value = default_value

    async def get_setting_value(self, licence_id: int) -> Union[Any, str]:
        """Retrieves the value

        Args:
            licence_id (int): the licence id

        Returns:
            int: server id
        """

        if not self.settings.get(licence_id):
            await self.update_setting_value(licence_id)

        category_id = self.settings.get(licence_id)

        return category_id

    async def update_setting_value(self, licence_id: int):
        """[Updates the value of given licence_id

        Args:
            licence_id (int): the licence id

        Raises:
            Exception: License id has no server
        """
        setting: LicenceSetting = await LicenceSetting.query.where(LicenceSetting.licence_id == licence_id).where(LicenceSetting.setting_id == self.setting_id).gino.first()

        if not setting:
            licence: Licence = await Licence.get(licence_id)
            if not licence:
                raise Exception(
                    f'License id doesnt exist - Setting {self.setting_id}')
            else:
                setting: LicenceSetting = await LicenceSetting.create(licence_id=licence_id, setting_id=self.setting_id, value=self.default_value)

        self.settings.update({licence_id: setting.value})
