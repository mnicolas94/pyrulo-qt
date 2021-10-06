from propsettings.configurable import register_as_setting
from propsettings.setting_types.range_setting_type import Range


class Base:
    pass


class A(Base):

    def __init__(self):
        self._a = 42

    def __str__(self):
        return "A"


class B(Base):

    def __init__(self):
        self._b = "dwqwdqw"

    def __str__(self):
        return "B"


class C(Base):

    def __init__(self):
        self._c = 0.2
        self._d = None

    def __str__(self):
        return "C"


register_as_setting(A, "_a")
register_as_setting(B, "_b")
register_as_setting(C, "_c", setting_type=Range)
register_as_setting(C, "_d", setting_value_type=B)
