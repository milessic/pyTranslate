from PyQt5.QtWidgets import (
        QHBoxLayout,
        QFrame,
        QLabel,
        QLineEdit,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QVBoxLayout,
        QWidget,
        QCheckBox,
        QComboBox,
        )
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class SettingsController(QWidget):
    fields = [
            #[
            #    "Use System Topbar (not recommended)",
            #    "combobox",
            #    "UseSystemTopBar",
            #    ["Yes", "No"]
            #    ],
            [
                "LangFrom",
                "input",
                "LangFrom",
            ],
            [
                "LangTo",
                "input",
                "LangTo",
            ],
            [
                "Disable Scrollbars",
                "combobox",
                "ScrollBarDisabled",
                ["Yes", "No"]
                ],
            [
                "Always on Top",
                "combobox",
                "AlwaysOnTop",
                ["Yes", "No"]
                ],
            [
                "LangFrom",
                "input",
                "LangFrom",
            ],
            [
                "Appearance",
                "combobox",
                "Theme",
                ["System"]
            ],
            [
                "Save History",
                "combobox",
                "SaveHistory",
                ["Yes", "No"]
            ],
            #[
            #    "Theme",
            #    "combobox",
            #    "Theme",
            #    ["System Default", "black"],
            #],
        ]
    dragging = False
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.icon_topnav_path = self.app.icon_topnav_path
        #self.setWindowIcon(self.app.icon)
        self.app_name = self.app.app_name + " Settings"
        self.initUi()


    def initUi(self):
        self.setWindowTitle(self.app_name)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)
        # set settings frame
        self.settings_frame = QFrame(self)
        self.main_layout.addWidget(self.settings_frame)
        self.setup_form()

    def setup_form(self):
        self.form_layout = QVBoxLayout(self.settings_frame)
        self.app_full_name = QLabel(self.app.short_description , self)
        self.form_layout.addWidget(self.app_full_name)
        for field in self.fields:
            field_layout = QHBoxLayout()
            field_label = QLabel(field[0], self)
            field_label.setFixedWidth(230)
            field_default_value = getattr(self.app.config,field[2])
            if isinstance(field_default_value, bool):
                match field_default_value:
                    case True:
                        field_default_value = "Yes"
                    case False:
                        field_default_value = "No"
            elif isinstance(field_default_value, int):
                field_default_value = str(field_default_value)
            match field[1]:
                case "checkbox":
                    element = QCheckBox(self)
                    element.setChecked(field_default_value)
                case "input":
                    element = QLineEdit(self)
                    element.setText(field_default_value)
                case "combobox":
                    element = QComboBox(self)
                    for opt in field[3]:
                        element.addItem(opt)
                    index = element.findText(field_default_value)
                    element.setCurrentIndex(index)
                case _:
                    QMessageBox.critical(self, "Error", f"Cannot set field '{field}'!")
                    return
            element.setObjectName(field[2])
            field.append(element)
            field_layout.addWidget(field_label)
            field_layout.addWidget(element)
            self.form_layout.addLayout(field_layout)
        self.buttons_layout = QHBoxLayout()
        self.form_btn = QPushButton("Save settings", self)
        self.form_btn.clicked.connect(self._update_config)
        self.form_btn.setMaximumWidth(150)
        self.settings_saved = QLabel("Settings saved", self)
        self.settings_saved.setStyleSheet("color: green")
        self.settings_saved.hide()
        self.buttons_layout.addWidget(self.form_btn, alignment=Qt.AlignLeft)
        self.buttons_layout.addWidget(self.settings_saved, alignment=Qt.AlignLeft)
        self.form_layout.addLayout(self.buttons_layout)

    def _update_config(self):
        # read inputs
        for field in self.fields:
            match field[1]:
                case "checkbox":
                    value = field[-1].isChecked()
                case "input":
                    value = field[-1].text()
                case "combobox":
                    value = field[-1].currentText()
                    if value.lower() == "yes":
                        value = True
                    elif value.lower() == "no":
                        value = False
                case _:
                    raise NotImplemented(f"Field type '{field[1]}' is not supported.")
            setattr(self.app.config, field[2], value)
        # save inputs
        self.app.config.update_config_file()
        # show user that it happened
        self.settings_saved.show()

    def _close(self):
        self.settings_saved.hide()
        self.destroy()

    def _minimize(self):
        pass

