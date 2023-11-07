from __future__ import annotations

import customtkinter as ctk
from PIL import Image

from common.constants import STRING
from scripts.be_management import BEMassDisenchant
from scripts.oe_management import ZeroSkinShards

# from scripts.settings_backup import BackupSettings, RestoreSettings
from scripts.skin_shards_stats import SkinCollectionStats, SkinShardsStats
from scripts.utilities import RemoveChallengeTokens, SetRandomIcon, CombineFragmentKeys

from .bases import FrameCategory, NavigationButton, Script
from .utils import open_git_repo_link, open_git_wiki_link

ctk.set_default_color_theme("./assets/theme/purple.json")


class HextechButEfficientApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hextech But Efficient")
        self.geometry("700x750")
        self.iconbitmap("./assets/icons/sivir_icon.ico")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = "./assets/images/"
        self.sivir_icon = ctk.CTkImage(Image.open(image_path + "sivir_icon.png"), size=(66, 66))
        self.sivir_part_splash = ctk.CTkImage(Image.open(image_path + "sivir_part_splash.png"), size=(415, 175))
        self.image_icon_image = ctk.CTkImage(Image.open(image_path + "image_icon_light.png"), size=(20, 20))
        self.home_image = ctk.CTkImage(
            light_image=Image.open(image_path + "home_dark.png"),
            dark_image=Image.open(image_path + "home_light.png"),
            size=(20, 20),
        )
        self.chat_image = ctk.CTkImage(
            light_image=Image.open(image_path + "chat_dark.png"),
            dark_image=Image.open(image_path + "chat_light.png"),
            size=(20, 20),
        )
        self.add_user_image = ctk.CTkImage(
            light_image=Image.open(image_path + "add_user_dark.png"),
            dark_image=Image.open(image_path + "add_user_light.png"),
            size=(20, 20),
        )

        # create navigation frame
        self.navigation_buttons: list[NavigationButton] = []

        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(6, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="Hextech\nBut\nEfficient",
            image=self.sivir_icon,
            compound="left",
            anchor="w",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=5, pady=5)

        self.home_button = NavigationButton(self, row=1, name="Home", image=self.home_image)
        self.be_management_button = NavigationButton(self, row=2, name="BE Management", image=self.chat_image)
        self.oe_management_button = NavigationButton(self, row=3, name="OE Management", image=self.chat_image)
        self.skin_shards_stats_button = NavigationButton(self, row=4, name="Skin Shards Stats", image=self.chat_image)
        self.utilities_button = NavigationButton(self, row=5, name="Utilities", image=self.add_user_image)

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, values=["Dark", "Light"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Text Box
        self.console_box = ctk.CTkTextbox(self, width=200, height=200)
        self.console_box.grid(row=6, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")
        self.console_box.configure(state="disabled")

        self.category_frames: list[FrameCategory] = []

        # 1 HOME
        self.home_frame = FrameCategory(self, self.home_button)
        self.home_frame.grid_rowconfigure(5, weight=1)
        self.home_frame.grid_columnconfigure(2, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.sivir_part_splash)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

        self.home_title = ctk.CTkTextbox(
            self.home_frame,
            width=500,
            height=20,
            bg_color="transparent",
            fg_color="transparent",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.home_title.insert("0.0", f"Hextech But Efficient, version: {STRING.VERSION}")
        self.home_title.grid(row=1, column=0, padx=20, pady=10, columnspan=2)
        self.home_title.configure(state="disabled")

        self.description_text = ctk.CTkTextbox(
            self.home_frame,
            width=500,
            height=150,
            bg_color="transparent",
            fg_color="transparent",
            font=ctk.CTkFont(size=13),
        )
        self.description_text.insert(
            "0.0",
            "League of Legends tool for quick & efficient management of some chores.\n"
            "Check links below to get more info on scripts.",
        )
        self.description_text.grid(row=2, column=0, padx=20, pady=10, columnspan=2)
        self.description_text.configure(state="disabled")

        self.github_button = ctk.CTkButton(
            self.home_frame,
            text="GitHub",
            image=self.image_icon_image,
            command=open_git_repo_link,
        )
        self.github_button.grid(row=2, column=0, padx=0, pady=0)

        self.wiki_button = ctk.CTkButton(
            self.home_frame,
            text="GitHub Wiki",
            image=self.image_icon_image,
            command=open_git_wiki_link,
        )
        self.wiki_button.grid(row=2, column=1, padx=20, pady=0)

        # 2 BE MANAGEMENT
        self.be_management = FrameCategory(
            self,
            self.be_management_button,
            Script("BE Mass Disenchant\naccounting for Mastery levels", BEMassDisenchant, self.image_icon_image),
        )

        # 3 OE MANAGEMENT
        self.oe_management = FrameCategory(
            self,
            self.oe_management_button,
            Script("Show skin shards for champs  without a skin", ZeroSkinShards, self.image_icon_image),
        )

        # 4 SKIN SHARDS STATS
        self.skin_shards_stats = FrameCategory(
            self,
            self.skin_shards_stats_button,
            Script("Skin Shards Stats", SkinShardsStats, self.image_icon_image),
            Script("Skin Collection Stats", SkinCollectionStats, self.image_icon_image),
        )

        # 5 UTILITIES
        self.utilities = FrameCategory(
            self,
            self.utilities_button,
            Script("Remove Challenge Tokens", RemoveChallengeTokens, self.image_icon_image),
            Script("Set Random Owned Icon", SetRandomIcon, self.image_icon_image),
            Script("Combine Fragment Keys", CombineFragmentKeys, self.image_icon_image),
        )

        # select default frame
        self.select_frame_by_name("Home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        for button in self.navigation_buttons:
            button.configure(fg_color=("gray75", "gray25") if button.name == name else "transparent")

        # show selected frame
        for category in self.category_frames:
            if name == category.name:
                category.grid(row=0, column=1, sticky="nsew")
            else:
                category.grid_forget()

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
