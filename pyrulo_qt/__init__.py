from propsettings_qt.setting_widget_retrieval import register_setting_type_drawer

from pyrulo_qt.selector_setting_drawer import ClassSelectorSettingDrawer
from pyrulo_qt.selector_setting_type import ClassSelector


register_setting_type_drawer(ClassSelector, ClassSelectorSettingDrawer)
