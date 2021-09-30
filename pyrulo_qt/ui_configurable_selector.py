import os
from PySide2 import QtWidgets, QtCore, QtGui
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

		self._custom_script_widget = QtWidgets.QWidget()
		custom_script_widget_layout = QtWidgets.QVBoxLayout()
		custom_script_widget_layout.setContentsMargins(0, 0, 0, 0)
		self._custom_script_widget.setLayout(custom_script_widget_layout)
		self._custom_script_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
		self._script_dir_widget = QtWidgets.QWidget()
		script_dir_widget_layout = QtWidgets.QHBoxLayout()
		script_dir_widget_layout.setContentsMargins(0, 0, 0, 0)
		self._script_dir_widget.setLayout(script_dir_widget_layout)
		self._script_dir_label = QtWidgets.QLabel()
		self._script_dir_label.setText(self.tr("Script not selected"))
		self._script_dir_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
		self._script_dir_button = QtWidgets.QPushButton()
		self._script_dir_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
		self._script_dir_button.clicked.connect(self._load_object_from_custom_script)
		self._script_dir_widget.layout().addWidget(self._script_dir_label)
		self._script_dir_widget.layout().addWidget(self._script_dir_button)
		self._script_class_name_label = QtWidgets.QLabel()
		self._script_class_name_label.setText(self.tr("None"))
		custom_script_widget_layout.addWidget(self._script_dir_widget)
		custom_script_widget_layout.addWidget(self._script_class_name_label)
		self._custom_script_widget.hide()
		layout.addWidget(self._custom_script_widget)

		self._collapsible_widget = QtWidgets.QWidget()
		collapsible_widget_layout = QtWidgets.QVBoxLayout()
		collapsible_widget_layout.setContentsMargins(0, 0, 0, 0)
		self._collapsible_widget.setLayout(collapsible_widget_layout)
		self._collapsible_widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
		layout.addWidget(self._collapsible_widget)

		self._conf_properties = SettingsAreaWidget()
		self._conf_properties.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
		self._collapsible_widget.layout().addWidget(self._conf_properties)

		self._collapsible_widget.hide()

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
			self._custom_script_widget.show()
		else:
			self._custom_script_widget.hide()

		self._current_index = index
		self._populate_current_object_properties()

	def _populate_current_object_properties(self):
		current_object = self.current_object()
		self._conf_properties.populate_object(current_object)
		if self._conf_properties.children_count > 0:
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
				self._custom_object = first_class()
				self._update_custom_script_texts(file_path, first_class.__name__)
			else:
				QtWidgets.QMessageBox.critical(
					self,
					self.tr("Error"),
					self.tr("Invalid script"),
					QtWidgets.QMessageBox.StandardButton.Ok)
		self._populate_current_object_properties()

	def _update_custom_script_texts(self, file_path, class_name):
		metrics = QtGui.QFontMetrics(self._script_dir_label.font())
		elided_text = metrics.elidedText(
			file_path,
			QtCore.Qt.TextElideMode.ElideMiddle,
			self._script_dir_label.width())
		self._script_dir_label.setText(elided_text)
		self._script_class_name_label.setText(class_name)

	def _disable_collapsible_feature(self):
		self._toggle_button.hide()
		self._collapsible_widget.hide()

	def _enable_collapsible_feature(self):
		self._toggle_button.show()

	@QtCore.Slot()
	def _collapse_or_expand(self, expand):
		arrow_type = QtCore.Qt.DownArrow if expand else QtCore.Qt.RightArrow
		self._toggle_button.setArrowType(arrow_type)
		if expand:
			self._collapsible_widget.show()
		else:
			self._collapsible_widget.hide()


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