from __future__ import annotations

import customtkinter as ctk
from PIL import Image

from common.constants import STRING
from scripts.be_management import BEMassDisenchant, BEMassOpening, BEDisenchantEverything
from scripts.oe_management import ZeroSkinShards

# from scripts.settings_backup import BackupSettings, RestoreSettings
from scripts.skin_shards_stats import SkinCollectionStats, SkinShardsStats
from scripts.utilities import CombineFragmentKeys, RemoveChallengeTokens, SetRandomIcon

from .const import IMAGE_PATH
from .elements import FrameCategory, NavigationButton, Script
from .utils import open_git_repo_link

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

        self.home_nav = NavigationButton(self, row=1, name="Home", image="home.png")
        self.be_management_nav = NavigationButton(self, row=2, name="BE Management", image="BE_icon.png")
        self.oe_management_nav = NavigationButton(self, row=3, name="OE Management", image="OE_icon.png")
        self.skin_shards_stats_nav = NavigationButton(self, row=4, name="Skin/Shard Stats", image="performing_arts.png")
        self.utilities_nav = NavigationButton(self, row=5, name="Utilities", image="utils.png")

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame, values=["Dark", "Light"], command=self.change_appearance_mode_event
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Text Box
        self.console_box = ctk.CTkTextbox(self, width=200, height=200, wrap="word")
        self.console_box.grid(row=6, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")
        self.console_box.insert("insert", "HextechButEfficient Console")
        self.console_box.configure(state="disabled")

        self.category_frames: list[FrameCategory] = []

        # 1 HOME
        self.home_frame = FrameCategory(self, self.home_nav)
        self.home_frame.grid_rowconfigure(5, weight=1)
        self.home_frame.grid_columnconfigure(1, weight=1)

        self.home_frame_large_image_label = ctk.CTkLabel(self.home_frame, text="", image=self.sivir_part_splash)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_title = ctk.CTkTextbox(
            self.home_frame,
            width=500,
            height=60,
            bg_color="transparent",
            fg_color="transparent",
            font=ctk.CTkFont(size=17, weight="bold"),
        )
        self.home_title.insert("0.0", f"Hextech But Efficient\nVersion: {STRING.VERSION}")
        self.home_title.grid(row=1, column=0, padx=20, pady=10)
        self.home_title.configure(state="disabled")

        self.description_text = ctk.CTkTextbox(
            self.home_frame,
            width=500,
            height=350,
            bg_color="transparent",
            fg_color="transparent",
            font=ctk.CTkFont(size=13),
        )
        self.description_text.insert(
            "0.0",
            (
                "League of Legends tool for quick & efficient management of some chores.\n\n"
                "Tutorial on how to use the tool.\n"
                "    * Open League Client.\n"
                "    * Choose a script from the tool to execute.\n"
                "    * Read information under '?' tooltip.\n"
                "    * Press 'Run' button.\n"
                "    * If the script has confirmation/output dialog press Yes/OK/No buttons there.\n"
                "    * The end. Console should print some success text.\n"
            ),
        )
        self.description_text.grid(row=2, column=0, padx=0, pady=0)
        self.description_text.configure(state="disabled")

        self.github_button = ctk.CTkButton(
            self.home_frame,
            width=280,
            height=56,
            text="GitHub (Source Repository)",
            font=ctk.CTkFont(size=17),
            image=ctk.CTkImage(Image.open(IMAGE_PATH + "github_mark.png"), size=(50, 50)),
            command=open_git_repo_link,
        )
        self.github_button.grid(row=2, column=0)

        # 2 BE MANAGEMENT
        self.be_management = FrameCategory(
            self,
            self.be_management_nav,
            Script("BE Mass Disenchant accounting for Mastery levels", BEMassDisenchant, "recycling_symbol.png"),
            Script("BE Related Loot Mass Opening", BEMassOpening, "door.png"),
            Script("BE Disenchant Everything", BEDisenchantEverything, "wastebasket.png"),
        )

        # 3 OE MANAGEMENT
        self.oe_management = FrameCategory(
            self,
            self.oe_management_nav,
            Script("Show skin shards for champs  without a skin", ZeroSkinShards, "keycap_digit_zero.png"),
        )

        # 4 SKIN SHARDS STATS
        self.skin_shards_stats = FrameCategory(
            self,
            self.skin_shards_stats_nav,
            Script("Skin Shards Stats", SkinShardsStats, "shark.png"),
            Script("Skin Collection Stats", SkinCollectionStats, "skis.png"),
        )

        # 5 UTILITIES
        self.utilities = FrameCategory(
            self,
            self.utilities_nav,
            Script("Remove Challenge Tokens", RemoveChallengeTokens, "no_entry.png"),
            Script("Set Random Owned Icon", SetRandomIcon, "framed_picture.png"),
            Script("Combine Fragment Keys", CombineFragmentKeys, "old_key.png"),
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
