"""
Confirmation box where the user needs to press Yes or No.

Implementation concept idea is largely looked in
* https://github.com/Akascape/CTkMessagebox 
    - Licenced with Creative Commons Zero v1.0 Universal

Well, I just wanted scrollable text inside those message boxes so I have to do my own implementation
However, we don't need most of features from CTkMessagebox extension so it's just ~100 lines of code.
"""


import platform

import customtkinter as ctk
from PIL import Image


class ConfirmationBox(ctk.CTkToplevel):
    """Represents Confirmation Box which can be

    * Yes/No choice for user to confirm the script
    * Ok confirmation if the script just outputs information without needing to confirm stuff.
    """

    def __init__(self, script_message: str, option_no: bool = True):
        super().__init__()
        self.option_no: bool = option_no

        self.title("Confirmation Dialog" if option_no else "Results Dialog")

        # they have an oversight bug in ctk so we need to set the icon after
        # https://stackoverflow.com/a/75825532/19217368
        self.after(201, lambda: self.iconbitmap("./assets/icons/sivir_icon.ico"))

        self.confirm: bool = False  # default is False in case user closes the dialog in other ways than Yes/No

        self.question = ctk.CTkButton(
            self,
            width=1,
            corner_radius=0,
            text="Do you confirm executing this script?" if option_no else "The output of the script is as follows",
            fg_color="transparent",
            hover=False,
            image=ctk.CTkImage(
                Image.open("assets/images/{}.png".format("question" if option_no else "info")), size=(66, 66)
            ),
        )
        self.question.grid(row=1, column=0, columnspan=6, sticky="nwes")

        # why custom font stuff is so weird x_x
        match platform.system():
            case "Windows":
                font = ctk.CTkFont("Consolas")
            case "Linux":
                font = ctk.CTkFont("courier")
            case "MacOS":
                font = ctk.CTkFont("Monaco")
            case _:
                font = ctk.CTkFont("Courier")

        self.script_info = ctk.CTkTextbox(self, width=500, height=400, wrap="word", font=font)

        self.script_info.insert("0.0", f"{script_message}")
        self.script_info.grid(row=2, column=0, columnspan=6, sticky="nwes")
        self.script_info.configure(state="disabled")

        # to make script info follow the resize motion
        self.grid_columnconfigure(0, weight=1, uniform="1")
        self.grid_rowconfigure(2, weight=1, uniform="1")

        # YES
        button_yes_text = "Yes" if option_no else "Ok"
        self.button_yes = ctk.CTkButton(self, text=button_yes_text, command=lambda: self.button_event(True))
        self.button_yes.grid(row=3, column=1, sticky="news", padx=10, pady=10)

        # NO
        if option_no:
            self.button_no = ctk.CTkButton(self, text="No", command=lambda: self.button_event(False))
            self.button_no.grid(row=3, column=2, sticky="news", padx=10, pady=10)

        self.bind("<Escape>", lambda _: self.button_event())

        if self.winfo_exists():
            self.grab_set()

    def get(self):
        if self.winfo_exists():
            self.master.wait_window(self)
        return self.confirm

    def button_event(self, event: bool = False):
        try:
            self.button_yes.configure(state="disabled")
            if self.option_no:
                self.button_no.configure(state="disabled")
        except AttributeError:
            pass

        self.grab_release()
        self.destroy()
        self.confirm = event
