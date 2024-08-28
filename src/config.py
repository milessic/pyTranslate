import configparser
from pathlib import Path
from getpass import getpass
import platform
import os
from pathlib import Path


class Config:
    default_config = """[DEFAULT]
AlwaysOnTop=1
LangFrom=pl
LangTo=de
Theme=black
StartX=1500
StartY=100
SaveHistory=1
UseSystemTopBar=0
ScrollBarDisabled=1
    """
    def __init__(self, app_path):
        self.platform = platform.system()
        self.pyclocks_path = Path(app_path)
        self.pyclocks_path.mkdir(parents=True, exist_ok=True)
        self.config_path = Path(self.pyclocks_path, ".pytranslate.ini")
        #case "Windows":
        #case "Darwin":
        self.c = configparser.ConfigParser()
        self.c.read(self.config_path)
        if len(self.c) != 1:
            del self.c
            print(self.config_path)
            print("Didn't detect valid config file, creating default one")
            with open(self.config_path, "w") as f:
                f.write(self.default_config)
            self.c = configparser.ConfigParser()
            self.c.read(self.config_path)

        # DEFAULT
        self.AlwaysOnTop = bool(int(self.c.get("DEFAULT", "AlwaysOnTop")))
        self.LangFrom= self.c["DEFAULT"]["LangFrom"]
        self.LangTo = self.c["DEFAULT"]["LangTo"]
        self.Theme = self.c["DEFAULT"]["Theme"]
        self.StartX = self.c["DEFAULT"]["StartX"]
        self.StartY = self.c["DEFAULT"]["StartY"]
        self.SaveHistory = bool(int(self.c.get("DEFAULT", "SaveHistory")))
        self.UseSystemTopBar = bool(int(self.c.get("DEFAULT", "UseSystemTopBar")))
        self.ScrollBarDisabled = bool(int(self.c.get("DEFAULT", "ScrollBarDisabled")))


    def _save_config(self):
        with open(self.config_path, "w") as f:
            self.c.write(f)

    def update_config_file(self):
        self._save_config()

    @property
    def AlwaysOnTop(self):
        return bool(int(self.c["DEFAULT"]["AlwaysOnTop"]))

    @AlwaysOnTop.setter
    def AlwaysOnTop(self, value):
        if value:
            self._AlwaysOnTop = "1"
        else:
            self._AlwaysOnTop = "0"
        self.c.set("DEFAULT", "AlwaysOnTop", self._AlwaysOnTop)

    @property
    def LangFrom(self):
        return self.c["DEFAULT"]["LangFrom"]

    @LangFrom.setter
    def LangFrom(self, value):
        self.c.set("DEFAULT", "LangFrom", value)
        self._save_config()

    @property
    def LangTo(self):
        return self.c["DEFAULT"]["LangTo"]

    @LangTo.setter
    def LangTo(self, value):
        self.c.set("DEFAULT", "LangTo", value)
        self._save_config()

    @property
    def StartX(self):
        return int(self.c["DEFAULT"]["StartX"])

    @StartX.setter
    def StartX(self, value):
        self.c.set("DEFAULT", "StartX", value)

    @property
    def StartY(self):
        return int(self.c["DEFAULT"]["StartY"])

    @StartY.setter
    def StartY(self, value):
        self.c.set("DEFAULT", "StartY", value)

    @property
    def SaveHistory(self):
        return bool(int(self.c["DEFAULT"]["SaveHistory"]))

    @SaveHistory.setter
    def SaveHistory(self, value:bool):
        if value:
            self._UseSystemTopBar = "1"
        else:
            self._UseSystemTopBar = "0"
        self.c.set("DEFAULT", "UseSystemTopBar", self._UseSystemTopBar)
    @property
    def UseSystemTopBar(self):
        return bool(int(self.c["DEFAULT"]["UseSystemTopBar"]))

    @UseSystemTopBar.setter
    def UseSystemTopBar(self, value:bool):
        if value:
            self._UseSystemTopBar = "1"
        else:
            self._UseSystemTopBar = "0"
        self.c.set("DEFAULT", "UseSystemTopBar", self._UseSystemTopBar)

    @property
    def ScrollBarDisabled(self):
        return bool(int(self.c["DEFAULT"]["ScrollBarDisabled"]))

    @ScrollBarDisabled.setter
    def ScrollBarDisabled(self, value:bool):
        if value:
            self._ScrollBarDisabled = "1"
        else:
            self._ScrollBarDisabled = "0"
        self.c.set("DEFAULT", "ScrollBarDisabled", self._ScrollBarDisabled)

