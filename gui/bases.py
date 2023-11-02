from __future__ import annotations

from typing import TYPE_CHECKING, Any, NamedTuple, Type

import customtkinter as ctk
from customtkinter.windows.widgets.image import CTkImage

from .utils import get_now_string

if TYPE_CHECKING:
    from common.connector import AluConnector

    from .app import HextechButEfficientApp


class Scripts(NamedTuple):
    name: str
    cls: Type[AluConnector]
    image: CTkImage


class ScriptTextBox(ctk.CTkTextbox):
    def __init__(
        self,
        master: Any,
        name: str,
        *,
        connector_cls: Type[AluConnector],
        row: int,
        column: int,
        image: ctk.CTkImage,
        console_box: ctk.CTkTextbox,
    ):
        super().__init__(master, bg_color="transparent", width=200, height=100)
        self.insert("0.0", name)
        self.grid(row=row, column=column, padx=20, pady=10)
        self.configure(state="disabled")

        self.name = name
        self.connector_cls = connector_cls
        self.console_box = console_box

        self.run_button = ctk.CTkButton(
            self,
            text="Run",
            image=image,
            compound="right",
            command=self.update_console_box,
            anchor="center",
        )
        self.run_button.place(in_=self, relx=0.5, rely=0.66, anchor="center")

    def update_console_box(self):
        # notification about pressing the button
        self.console_box.configure(state="normal")
        self.console_box.insert("insert", f'{get_now_string()} | Starting "{self.name}"\n')
        self.console_box.configure(state="disabled")
        self.console_box.update()
        self.console_box.see("end")

        connector = self.connector_cls()
        connector.start()

        # call the script and print the result
        self.console_box.configure(state="normal")
        self.console_box.insert("insert", f"{get_now_string()} | {connector.result}\n")
        self.console_box.configure(state="disabled")
        self.console_box.see("end")


class NavigationButton(ctk.CTkButton):
    def __init__(
        self,
        app: HextechButEfficientApp,
        *,
        row: int,
        name: str = "CTkButton",
        image: CTkImage | Any | None = None,
    ):
        super().__init__(
            app.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text=name,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=image,
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
    def __init__(self, master: HextechButEfficientApp, button: NavigationButton, *scripts: Scripts):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent",
        )
        master.category_frames.append(self)
        self.name = button.name

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
