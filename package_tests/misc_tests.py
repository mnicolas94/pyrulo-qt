from pyrulo import class_imports

from pyrulo_qt.ui_configurable_selector import ConfigurableSelector
from package_tests.test_classes import Base


if __name__ == '__main__':
    import os
    import sys
    from pathlib import Path
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QWidget, QVBoxLayout

    app = QApplication(sys.argv)

    window = QWidget()
    window.setMinimumSize(100, 100)
    layout = QVBoxLayout()
    window.setLayout(layout)

    classes_path = str(Path(__file__).parent)
    class_imports.register_classes_dir_by_key("key", classes_path, Base, False)

    # selector = ConfigurableSelector("key")
    selector = ConfigurableSelector(base_class=Base)
    layout.addWidget(selector)

    window.show()

    sys.exit(app.exec_())
