import sys
import configparser
import translators
from tkinter import (
    END, Tk, StringVar, Label, Entry, Button, Frame, Toplevel, filedialog, messagebox, ttk, Misc, Text, font, PhotoImage,
        )


class BlackTheme:
    bg = "#000000"
    highlight = "#1a1a1a"
    fg = "#ffffff"
    txt_bg = "#2b2b2b"
    txt_fg = "#eaeaea"
    btn_highlight = "#4d4d4d"
    status_bg = "#151515"

class WhiteTheme:
    bg = "#ffffff"
    highlight = "#f2f2f2"
    fg = "#000000"
    txt_bg = "#e6e6e6"
    txt_fg = "#333333"
    btn_highlight = "#cccccc"
    status_bg = "#f7f7f7"

class BlueTheme:
    bg = "#007acc"
    highlight = "#005999"
    fg = "#ffffff"
    txt_bg = "#cce7ff"
    txt_fg = "#003366"
    btn_highlight = "#66b2ff"
    status_bg = "#004080"

class RedTheme:
    bg = "#b30000"
    highlight = "#800000"
    fg = "#ffffff"
    txt_bg = "#ffcccc"
    txt_fg = "#330000"
    btn_highlight = "#ff6666"
    status_bg = "#660000"

class DarkBlueTheme:
    bg = "#22303c"
    highlight = "#9DB2BF"
    fg = "#ffffff"
    txt_bg ="#FFFDFA" 
    txt_fg ="#15202b" 
    btn_highlight="#ffffff"
    status_bg = "#6b6967"

class PastelTheme:
    bg = "#ffd1dc"
    highlight = "#ffb3c1"
    fg = "#4b0082"
    txt_bg = "#fff0f5"
    txt_fg = "#800080"
    btn_highlight = "#ff69b4"
    status_bg = "#ff80bf"



selectedStyle = DarkBlueTheme
class Styles:
    def __init__(self, theme_name:str):
        default_theme = BlackTheme
        match theme_name.lower():
            case "darkblue":
                stylesheet = DarkBlueTheme
            case "lightgray":
                stylesheet = LightGrayTheme 
            case "black":
                stylesheet = BlackTheme
            case "white":
                stylesheet = WhiteTheme
            case "blue":
                stylesheet = BlueTheme
            case "red":
                stylesheet = RedTheme
            case "pastel":
                stylesheet = PastelTheme
            case "none":
                stylesheet = default_theme
            case _:
                print(f"Theme not supported - '{theme_name}'!")
                stylesheet = default_theme
        for k,v in stylesheet.__dict__.items():
            if k.startswith("__"):
                continue
            setattr(self, k,v)


class PyTranslate(Tk):
    def __init__(self, theme:str | None = None, lang_from:str="pl", lang_to:str="de"):
        super().__init__()
        self.history_file = ".history"
        self.click_x = 0
        self.click_y = 0
        self.ts = translators
        self.pixel = PhotoImage()
        self.helv13 = font.Font(family='Helvetica', size=13) 
        self.helv5 = font.Font(family='Helvetica', size=5, weight='bold')
        self.nerd5 = font.Font(family="NerdFont", size=6)
        theme = str(theme)
        #self.resizable(0, 0) 
        self.s = Styles(theme_name=theme)
        self.config(bg=self.s.bg)
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.name = "pyTranslate"
        self.root = self#Toplevel(self)
        self.w = 367
        self.h = 100
        self.ws = int(self.winfo_screenwidth() - self.w*1.5)
        self.hs = int(self.winfo_screenheight()/2 - self.h*3)
        self.root.geometry(f"{self.w}x{self.h}+{self.ws}+{self.hs}")
        #self.root.overrideredirect(True)


        self.initUi()
        self.update()
        #self.wm_attributes('-type', 'splash')
        #self.wm_attributes('-fullscreen', 'True')



    def initUi(self):
        self.title(self.name)
        # setup top
        self.lang_from_entry = self.myEntry(self.root, width=10, font=self.helv13, bg=self.s.bg)
        self.switch_lang_btn = self.myButton(self.root, "",command=self._switch_lang, font=self.nerd5)
        self.lang_to_entry = self.myEntry(self.root, width=10, font=self.helv13)
        self.go_btn = self.myButton(self.root, "Search!", command=self._search, font=self.nerd5)
        self.exit_btn = self.myButton(self.root, "", self._close, width=3, font=self.nerd5)
        self.exit_btn.configure(borderwidth=0, highlightcolor=self.s.bg, highlightbackground=self.s.bg)
        self.lang_from_entry.grid(row=1, column=0, pady=5)
        self.switch_lang_btn.grid(row=1, column=1)
        self.lang_to_entry.grid(row=1, column=3)
        self.go_btn.grid(row=1, column=2)
        self.exit_btn.place(x=330, y=3)
        self._insert_langs()
        # setup bottom
        self.input_entry = self.myText(self.root, width=20, font=self.helv13)
        self.input_entry.bind("<Return>", self._input_event)
        self.input_entry.bind("<Control-BackSpace>", self._input_clear)
        self.bind("<Control-r>", self._switch_input_output_event)
        self.bind("<Control-R>", self._switch_input_output_event_R)
        self.bind("<Control-q>", self._exit_event)
        self.bind("<B1-Motion>", self._move)
        self.bind("<Button-1>", self._click)
        #self.input_entry.bind("<Control-a>",  self._select_a_input)
        self.output_entry = self.myText(self.root, width=20, font=self.helv13)
        self.input_entry.grid(row=2, column=0, columnspan=2)
        self.output_entry.grid(row=2, column=2, columnspan=2)
        self.input_entry.focus()

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

    def _exit_event(self, event):
        self.destroy()

    def _switch_input_output_event(self, event):
        self._switch_lang()

    def _switch_input_output_event_R(self, event):
        self._switch_input_output()

    def _input_event(self, event):
        self._search()

    def _select_a_input(self, event):
        # or more universal
        # select text after 50ms
        self.after(50, self._select_all, self.input_entry)

    def _select_all(self, widget):
        widget.select_range("1.0", END)
        widget.icursor(END)

    def _input_clear(self, event):
        self.input_entry.delete("1.0", END)

    def _search(self):
        self.lang_from = self.lang_from_entry.get()
        self.lang_to = self.lang_to_entry.get()
        if not self.lang_from or not self.lang_to:
            messagebox.showerror(title=self.name, message="Both language from and language to have to be filled!")
            return
        source_text = self.input_entry.get("1.0", END)
        try:
            translation = self.ts.translate_text(query_text=source_text, from_language=self.lang_from, to_language=self.lang_to)
        except Exception as e:
            messagebox.showerror(title=self.name + f": {type(e).__name__}", message=str(e))
        self.output_entry.delete("1.0", END)
        self.output_entry.insert("1.0",translation)
        self._save_to_history()

    def _switch_lang(self):
        # clear fields
        # switch languanges
        self.lang_from, self.lang_to = self.lang_to, self.lang_from
        # insert text
        self._insert_langs()
        self._switch_input_output()

    def _insert_langs(self):
        self.lang_to_entry.delete(0, END)
        self.lang_from_entry.delete(0,END)
        self.lang_to_entry.insert(0, self.lang_to)
        self.lang_from_entry.insert(0, self.lang_from)

    def _switch_input_output(self):
        # swap
        txt_in = self.input_entry.get("1.0", END)
        txt_out = self.output_entry.get("1.0", END)
        # clear
        self.input_entry.delete("1.0", END)
        self.output_entry.delete("1.0", END)
        # insert
        self.input_entry.insert("1.0", txt_out)
        self.output_entry.insert("1.0", txt_in)
    
    def _save_to_history(self):
        with open(self.history_file,"a") as f:
            f.write(f"""{self.lang_from},{self.lang_to},{self.input_entry.get("1.0", END)},{self.output_entry.get("1.0", END)}""")

    def myText(self, master:Misc, height=4, **kwargs) -> Text:
        return Text(
                master=master,
            background=self.s.txt_bg,
            highlightcolor=self.s.bg,
            highlightbackground=self.s.bg,
            fg=self.s.txt_fg,
            height=height,
            border=0,
            **kwargs
                )
    def myEntry(self, master:Misc,fg:str|None=None, bg:str|None=None,**kwargs) -> Entry:
        fg = fg if fg is not None else self.s.txt_fg
        bg = bg if bg is not None else self.s.bg
        return Entry(
            master=master,
            background=bg,
            highlightcolor=bg,
            highlightbackground=bg,
            fg=self.s.txt_fg,
            border=0,
            **kwargs
            )
    def myButton(self, master, text:str, command, fg=None, bg=None, width=30, height=6, **kwargs) -> Button:
        return Button(
                image=self.pixel,
                master=master,
                text=text,
                command=command,
                compound="center",
                background=self.s.bg if bg is None else bg,
                fg=self.s.fg if fg is None else fg,
                highlightcolor=self.s.btn_highlight,
                highlightbackground=self.s.btn_highlight,
                activebackground=self.s.btn_highlight,
                width=width,
                height=height,
                #**kwargs
                )

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(".pytranslate.ini")

    try:
        not_on_top = config["DEFAULT"]["NotOnTop"]
    except KeyError:
        not_on_top = False
    finally:
        if "--not-on-top" in sys.argv:
            not_on_top = True
    try:
        lang_from = config["DEFAULT"]["LangFrom"]
    except KeyError as e:
        print(e)
        lang_from = "pl" 
    try:
        lang_to = config["DEFAULT"]["LangTo"]
        print(lang_to)
    except KeyError:
        lang_to = "de"
    try:
        theme = config["DEFAULT"]["Theme"]
    except KeyError:
        theme = "black"
    langs = []
    for arg in sys.argv:
        if arg.startswith("-"):
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
    app = PyTranslate(
            lang_from=lang_from,
            lang_to=lang_to,
            theme=theme
            )
    if not not_on_top:
        app.attributes("-topmost", True)
    app.mainloop()

