from __future__ import annotations

import inspect
import threading
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TYPE_CHECKING, NamedTuple, Optional, Type

import customtkinter as ctk
from PIL import Image

from .bases import CreateToolTip
from .const import IMAGE_PATH
from .utils import get_now_string

if TYPE_CHECKING:
    from common.connector import AluConnector

    from .app import HextechButEfficientApp


class Script(NamedTuple):
    name: str
    cls: Type[AluConnector]
    image: str


class ScriptTextBox(ctk.CTkTextbox):
    def __init__(
        self,
        master: FrameCategory,
        name: str,
        *,
        connector_cls: Type[AluConnector],
        row: int,
        column: int,
        image: str,
        console_box: ctk.CTkTextbox,
    ):
        super().__init__(master, bg_color="transparent", width=200, height=100)
        self.insert("0.0", name)
        self.grid(row=row, column=column, padx=20, pady=10)
        self.configure(state="disabled")

        self.master: FrameCategory = master
        self.name: str = name
        self.connector_cls: Type[AluConnector] = connector_cls
        self.console_box: ctk.CTkTextbox = console_box

        self.info_button = ctk.CTkButton(
            self,
            text="?",
            compound="right",
            anchor="center",
            width=12,
            height=12,
            corner_radius=7,
        )
        self.info_button.place(in_=self, relx=0.95, rely=0.12, anchor="center")
        CreateToolTip(
            self.info_button,
            inspect.cleandoc(connector_cls.__doc__ or "Sorry, no information provided about this feature."),
        )

        self.run_button = ctk.CTkButton(
            self,
            width=150,
            height=33,
            text="Run",
            image=ctk.CTkImage(Image.open(IMAGE_PATH + image), size=(25, 25)),
            compound="right",
            command=self.update_console_box,
            anchor="center",
        )
        self.run_button.place(in_=self, relx=0.5, rely=0.66, anchor="center")

    def update_console_box(self):
        # idk how to update the cursor - it just does not work
        # self.master.master.config(cursor="watch")
        the_prefix = f"\n{get_now_string()} | {self.name} | "
        # notification about pressing the button
        self.console_box.configure(state="normal")
        self.console_box.insert("insert", f"{the_prefix} Starting")
        self.console_box.configure(state="disabled")
        self.console_box.update()
        self.console_box.see("end")

        connector = self.connector_cls(need_confirmation=True)
        connector.start()

        # self.master.master.config(cursor="arrow")
        # ^this should be in body of ConfirmationBox as self.master.config(cursor="arrow")

        # call the script and print the result
        self.console_box.configure(state="normal")
        self.console_box.insert("insert", f"{the_prefix} {connector.console_text}")
        self.console_box.configure(state="disabled")
        self.console_box.see("end")


class NavigationButton(ctk.CTkButton):
    def __init__(
        self,
        app: HextechButEfficientApp,
        *,
        row: int,
        name: str = "CTkButton",
        image: str,
        dark_image: Optional[str] = None,
    ):
        ctk_image = ctk.CTkImage(
            light_image=Image.open(IMAGE_PATH + image),
            dark_image=Image.open(IMAGE_PATH + dark_image)
            if dark_image
            else None,  # type:ignore # it can be None. Just look at doc string of CTkImage
            size=(25, 25),
        )

        super().__init__(
            app.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=name,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=ctk_image,
            anchor="w",
            command=self.callback,
        )
        self.name = name
        self.app = app
        self.grid(row=row, column=0, sticky="ew")
        app.navigation_buttons.append(self)

    def callback(self):
        self.app.select_frame_by_name(self.name)


class FrameCategory(ctk.CTkFrame):
    if TYPE_CHECKING:
        master: HextechButEfficientApp

    def __init__(self, master: HextechButEfficientApp, button: NavigationButton, *scripts: Script):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent",
        )
        master.category_frames.append(self)
        self.name: str = button.name

        self.scripts = []
        for index, script in enumerate(scripts):
            self.scripts.append(
                ScriptTextBox(
                    self,
                    script.name,
                    row=index // 2,
                    column=index % 2,
                    connector_cls=script.cls,
                    image=script.image,
                    console_box=master.console_box,
                )
            )
