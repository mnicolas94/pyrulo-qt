import os
from PySide2 import QtWidgets, QtCore
from propsettings_qt.ui_settings_area import SettingsAreaWidget
from pyrulo import class_imports


class ConfigurableSelector(QtWidgets.QWidget):
	"""
	Widget para cargar clases que hereden de una clase base especificada
	e inicializar un combobox con instancias de dichas clases. Consta de dos elementos agrupados en un vertical layout.
	El primero es el combobox. El segundo es un area para configurar las uiproperties del objeto seleccionado.
	"""
	eventObjectSelected = QtCore.Signal(object)

	def __init__(self, dir_key, parent=None):
		super(ConfigurableSelector, self).__init__(parent)
		self._dir_key = dir_key
		self._objects = []
		self._custom_object = None
		self._current_index = 0

		layout = QtWidgets.QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		self.setLayout(layout)

		self._toggle_button = QtWidgets.QToolButton()
		self._toggle_button.setStyleSheet("QToolButton { border: none; }")
		self._toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
		self._toggle_button.setArrowType(QtCore.Qt.RightArrow)
		self._toggle_button.setCheckable(True)
		self._toggle_button.setChecked(False)
		self._toggle_button.clicked.connect(self._collapse_or_expand)

		self._combobox = QtWidgets.QComboBox(self)
		self._combobox.currentIndexChanged.connect(self._selection_changed)
		self._combobox.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)

		combobox_containter = QtWidgets.QWidget()
		combobox_containter_layout = QtWidgets.QHBoxLayout()
		combobox_containter_layout.setContentsMargins(0, 0, 0, 0)
		combobox_containter.setLayout(combobox_containter_layout)
		combobox_containter_layout.addWidget(self._toggle_button)
		combobox_containter_layout.addWidget(self._combobox)
		layout.addWidget(combobox_containter)

		self._conf_properties = SettingsAreaWidget()
		self._conf_properties.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
		self._conf_properties.hide()
		self.layout().addWidget(self._conf_properties)

		self._populate_objects()

	def current_object(self):
		objects_count = len(self._objects)
		if objects_count > 0:
			if self._current_index == objects_count:
				return self._custom_object
			else:
				return self._objects[self._current_index]
		else:
			return None

	def populate_class(self, dir_key):
		"""
		Inicializar el combobox con una nueva clase.
		:param class_dir:
		:param clazz:
		:return:
		"""
		self._dir_key = dir_key
		self._populate_objects()

	def _populate_objects(self):
		"""
		Inicializar el combobox.
		:return:
		"""
		self._clear_objects()
		classes = class_imports.import_classes_by_key(self._dir_key)
		classes = sorted(classes, key=lambda cls: str(cls))
		for cls in classes:
			instance = cls()
			self._objects.append(instance)
			self._combobox.addItem(str(instance))
		self._combobox.addItem(self.tr("Custom script..."))
		self.eventObjectSelected.emit(self.current_object())

	def _clear_objects(self):
		self._objects.clear()
		self._custom_object = None
		self._combobox.clear()
		self._conf_properties.clear()

	def _selection_changed(self, index):
		if index == len(self._objects):
			custom_object = self._load_object_from_custom_script()
			if custom_object is None:
				self._combobox.setCurrentIndex(self._current_index)
				return
			self._custom_object = custom_object

		self._current_index = index
		current_object = self.current_object()
		self._conf_properties.populate_configurations(current_object)
		if self._conf_properties.settings_count > 0:
			self._enable_collapsible_feature()
		else:
			self._disable_collapsible_feature()
		self.eventObjectSelected.emit(current_object)

	def _load_object_from_custom_script(self):
		file_path, file_filter = QtWidgets.QFileDialog.getOpenFileName(
			self,
			self.tr("Select custom script"),
			os.getcwd(),
			"Python script (*.py)"
		)
		if file_path != "":
			classes = class_imports.import_classes_in_specific_script_by_key(file_path, self._dir_key)
			if len(classes) > 0:
				first_class = classes[0]
				return first_class()
			else:
				QtWidgets.QErrorMessage.showMessage(self.tr("Invalid script"))
				return None
		else:
			return None

	def _disable_collapsible_feature(self):
		self._toggle_button.hide()
		self._conf_properties.hide()

	def _enable_collapsible_feature(self):
		self._toggle_button.show()

	@QtCore.Slot()
	def _collapse_or_expand(self, expand):
		arrow_type = QtCore.Qt.DownArrow if expand else QtCore.Qt.RightArrow
		self._toggle_button.setArrowType(arrow_type)
		if expand:
			self._conf_properties.show()
		else:
			self._conf_properties.hide()


if __name__ == '__main__':
	import sys
	from PySide2.QtWidgets import QApplication
	from PySide2.QtWidgets import QWidget, QVBoxLayout

	app = QApplication(sys.argv)

	window = QWidget()
	window.setMinimumSize(100, 100)
	layout = QVBoxLayout()
	window.setLayout(layout)

	selector = ConfigurableSelector("iu")
	layout.addWidget(selector)

	window.show()

	sys.exit(app.exec_())