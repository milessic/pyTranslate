# About
Visit [Webpage](https://milessic.github.io/pyTranslate/) for downloads

pyTranslate is a small project that was created to have simple and small translator window always on top during education.

App usses [UlionTse/translaors](https://github.com/UlionTse/translators) as backend for translation services.

# Start
To start app execute it as a python script, additionally you may add options:
```
[options] [lang_from] [lang_to] - start app with specific languages set
--not-on-top         - app is not always on top
--dont-save-history  - dont save history for this session 

examples:
python3 transalte.py en de  <- starts with lang_from: en and lang_to: de 
python translate.py --not-on-top  <- starts with default languages, app is not on top
python translate.py --not-on-top pl ja  <- starts with pl to ja languages, app is not on top,

```

# History
By default app saves history, if you want or need, there is a possibility to disable it by putting ``SaveHistory=0`` in ``.pytranslate.ini``


# Environment Setup
- install python (and pyqt5)
- install requirements.txt

# Settings
All settings can be set in ``.pytransalte.ini`` file, that should be placed under ``$HOME`` directory, but app can be run with system arguments, like ``--not-on-top`` that will temporary override settings from config file

> [!WARNING]
> This app is not meant for commercial use!
> For commercial usage, buy commercial translate license

Example .pytranslate.ini
```
[DEFAULT]
NotOnTop=0
LangFrom=pl
LangTo=de
Theme=black
StartX=1500
StartY=100
SaveHistory=1
```
