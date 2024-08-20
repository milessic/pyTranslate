import json
import sys
import os
import configparser
import translators
from PyQt5.QtWidgets import (
        QWidget,
        QApplication,
        QMainWindow,
        QSplitter,
        QLabel,
        QLineEdit,
        QPlainTextEdit,
        QPushButton,
        QVBoxLayout,
        QHBoxLayout,
        QFrame,
        QMessageBox,
        )
from PyQt5.QtCore import QLine, Qt, QPoint


class PyTranslate(QMainWindow):
    control_pressed = False
    shift_pressed = False
    dragging = False
    drag_position = None
    history_file_path = f"{os.getenv('HOME')}/.pytranslate.history.json"
    def __init__(self, theme:str | None = None, lang_from:str="pl", lang_to:str="de", always_on_top:bool=True, start_pos:None|tuple=None, save_history:bool=True):
        super().__init__()
        self.save_history = save_history
        self.click_x = 0
        self.click_y = 0
        self.ts = translators
        theme = str(theme)
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.name = "pyTranslate"
        self.w = 327
        self.h = 100
        self.ws = 300 if start_pos is None else start_pos[0]
        self.hs = 100 if start_pos is None else start_pos[1]

        self.setGeometry(self.ws, self.hs, self.w+self.pos().x(), self.h)


        self.initUi()
        self.update()
        if always_on_top:
            self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint)
        self.input_entry.setFocus()
        self.show()

    def initUi(self):
        self.setWindowTitle(self.name)
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)
        # setup top
        self.top_layout = QHBoxLayout()
        self.lang_from_entry = self.myQLineEdit(self, width=10)
        self.switch_lang_btn = self.myQPushButton(self, "",command=self._switch_lang)
        self.lang_to_entry = self.myQLineEdit(self, width=10)
        self.go_btn = self.myQPushButton(self, "Go!", command=self._search)
        self.exit_btn = self.myQPushButton(self, "", self._close)
        self.top_layout.addWidget(self.lang_from_entry)
        self.top_layout.addWidget(self.switch_lang_btn)
        self.top_layout.addWidget(self.go_btn)
        self.top_layout.addWidget(self.lang_to_entry)
        self.top_layout.addWidget(self.exit_btn)
        self.main_layout.addLayout(self.top_layout)
        self._insert_langs()
        # setup bottom
        self.bottom_layout = QHBoxLayout()
        self.entries_divider = QSplitter(Qt.Horizontal, self)
        self.input_entry = self.myQPlainTextEdit(self, width=20)
        self.output_entry = self.myQPlainTextEdit(self, width=20)
        self.entries_divider.addWidget(self.input_entry)
        self.entries_divider.addWidget(self.output_entry)
        self.bottom_layout.addWidget(self.entries_divider)
        self.main_layout.addLayout(self.bottom_layout)

    # events
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.control_pressed = False
        if e.key() == Qt.Key_Shift:
            self.shift_pressed = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Control:
            self.control_pressed = True
        if e.key() == Qt.Key_Shift:
            self.shift_pressed = True

        if self.control_pressed:
            if e.key() == Qt.Key_R:
                if self.shift_pressed:
                    self._switch_input_output_event_R(e)
                else:
                    self._switch_input_output_event(e)
            if e.key() == Qt.Key_Q:
                self._exit()
        if e.key() == Qt.Key_Return:
            self._search()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = e.globalPos() - self.frameGeometry().topLeft()
            e.accept()

    def mouseMoveEvent(self, e):
        if self.dragging:
            self.move(e.globalPos() - self.drag_position)
            e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.dragging = False
            e.accept()


    # methods

    def _focus_input_entry(self, event):
        self.input_entry.focus()

    def _close(self, event=None):
        exit()

    def _click(self, event):
        self.click_x, self.click_y = event.x, event.y

    def _move(self, event):
        x, y = self.winfo_pointerxy()
        x_rel, y_rel = x-self.click_x, y-self.click_y
        self.geometry(f"+{x_rel}+{y_rel}")

    def _exit(self):
        exit()

    def _switch_input_output_event(self, event):
        self._switch_lang()

    def _switch_input_output_event_R(self, event):
        self._switch_input_output()

    def _input_event(self, event):
        self._search()


    def _search(self):
        self.lang_from = self.lang_from_entry.text()
        self.lang_to = self.lang_to_entry.text()
        if not self.lang_from or not self.lang_to:
            messagebox.showerror(title=self.name, message="Both language from and language to have to be filled!")
            return
        source_text = self.input_entry.toPlainText()
        try:
            translation = self.ts.translate_text(query_text=source_text, from_language=self.lang_from, to_language=self.lang_to)
        except Exception as e:
            messagebox.showerror(title=self.name + f": {type(e).__name__}", message=str(e))
        self.output_entry.clear()
        self.output_entry.insertPlainText(translation)
        self._save_to_history()

    def _switch_lang(self):
        # clear fields
        # switch languanges
        self.lang_from, self.lang_to = self.lang_to, self.lang_from
        # insert text
        self._insert_langs()
        self._switch_input_output()

    def _insert_langs(self):
        self.lang_to_entry.clear()
        self.lang_from_entry.clear()
        self.lang_to_entry.setText(self.lang_to)
        self.lang_from_entry.setText(self.lang_from)

    def _switch_input_output(self):
        # swap
        txt_in = self.input_entry.toPlainText()
        txt_out = self.output_entry.toPlainText()
        # clear
        self.input_entry.clear()
        self.output_entry.clear()
        # insert
        self.input_entry.insertPlainText(txt_out)
        self.output_entry.insertPlainText(txt_in)
    
    def _save_to_history(self):
        if not self.save_history:
            return
        try:
            history_file = json.load(open(self.history_file_path, "r"))
        except Exception as e:
            print(e)
            QMessageBox.critical(self, "Error", "Could not load history file!")
            history_file = []
        history_file.append([self.lang_from, self.lang_to, self.input_entry.toPlainText(), self.output_entry.toPlainText()])
        json.dump(history_file, open(self.history_file_path, "w"), indent=4)

    def myQPlainTextEdit(self, parent, height=4, **kwargs) -> QPlainTextEdit:
        text = QPlainTextEdit(
                parent=parent,
                #**kwargs
                )
        text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        text.setStyleSheet(f"""
        border:none;
        background: transparent;
        """)
        return text

    def myQLineEdit(self, parent,**kwargs) -> QLineEdit:
        qlineedit= QLineEdit(
            parent,
            #**kwargs
            )
        qlineedit.setStyleSheet("""
        border:none;
        background:transparent;
        """)
        return qlineedit

    def myQPushButton(self, parent, text:str, command,width=30, height=30, **kwargs) -> QPushButton:
        btn = QPushButton(
                text,
                parent,
                #**kwargs
                )
        btn.setFixedWidth(width)
        btn.setFixedHeight(height)
        btn.clicked.connect(command)
        btn.setStyleSheet("""
        border: none;
        color: palette(window-text);
        background: transparent;
        """)

        return btn

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(f"{os.getenv('HOME')}/.pytranslate.ini")

    try:
        not_on_top = bool(int(config["DEFAULT"]["NotOnTop"]))
    except KeyError:
        not_on_top = False
    finally:
        if "--not-on-top" in sys.argv:
            not_on_top = True
    try:
        lang_from = config["DEFAULT"]["LangFrom"]
    except KeyError as e:
        lang_from = "pl" 
    try:
        lang_to = config["DEFAULT"]["LangTo"]
    except KeyError:
        lang_to = "de"
    try:
        theme = config["DEFAULT"]["Theme"]
    except KeyError:
        theme = "black"
    try:
        start_x = int(config["DEFAULT"]["StartX"])
    except:
        start_x = 100
    try:
        start_y = int(config["DEFAULT"]["StartY"])
    except:
        start_y = 100
    try:
        save_history= bool(int(config["DEFAULT"]["SaveHistory"]))
    except:
        save_history = True
    langs = []
    for arg in sys.argv:
        if arg.startswith("-"):
            if arg == "--dont-save-history":
                save_history = False
            continue
        if arg.endswith(".py"):
            continue
        langs.append(arg)

    if len(langs) == 2:
        lang_from = langs[0]
        lang_to = langs[1]
    elif not len(langs):
        pass
    else:
        raise IndexError(f"Provided langs number have to be exactly 2 but {len(langs)} provided! - {langs}")


    # start app
    app = QApplication(sys.argv)
    window = PyTranslate(
            lang_from=lang_from,
            lang_to=lang_to,
            theme=theme,
            always_on_top=not_on_top,
            start_pos=(start_x, start_y),
            save_history=save_history,
            )
    window.show()
    sys.exit(app.exec_())


