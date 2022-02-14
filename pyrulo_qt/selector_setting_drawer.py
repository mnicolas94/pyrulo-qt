from propsettings.setting import Setting
from propsettings_qt.setting_drawers.setting_drawer import SettingDrawer
from pyrulo_qt.ui_configurable_selector import ConfigurableSelector

from pyrulo_qt.selector_setting_type import ClassSelector


class ClassSelectorSettingDrawer(SettingDrawer):

    def __init__(self, selector: ClassSelector, setting_owner, setting: Setting):
        super(ClassSelectorSettingDrawer, self).__init__(setting_owner, setting)
        self._selector = selector

        self._selector_widget = DrawerConfigurableSelector(self, base_class=self._selector.base_class)
        self._selector_widget.eventObjectSelected.connect(self._on_object_selected)
        self._update_ui_from_value()

    def get_widget(self):
        return self._selector_widget

    def _update_ui_from_value(self):
        value = self._get_value()
        value_class = type(value)
        self._selector_widget.add_class(value_class)
        self._selector_widget.set_object_for_class(value_class, value)
        self._selector_widget.select_class(value_class)

    def _on_object_selected(self, obj):
        self._set_value(obj)


class DrawerConfigurableSelector(ConfigurableSelector):

    def __init__(self, drawer, **kwargs):
        super(DrawerConfigurableSelector, self).__init__(**kwargs)
        self._drawer = drawer