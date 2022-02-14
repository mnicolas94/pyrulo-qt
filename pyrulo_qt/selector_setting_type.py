from propsettings.setting_type import SettingType


class ClassSelector(SettingType):

    def __init__(self, base_class):
        self._base_class = base_class

    @property
    def base_class(self):
        return self._base_class
