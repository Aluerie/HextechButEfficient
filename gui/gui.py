import dearpygui.dearpygui as dpg

from scripts.be_management.be_mass_disenchant import be_mass_disenchant_button
from scripts.oe_management.show_zero_skins_shards import show_zero_skins_shards_button
from scripts.remove_challenges_tokens.remove_challenges_tokens import remove_challenges_tokens_button


def run_gui():
    dpg.create_context()
    with dpg.font_registry():
        # first argument ids the path to the .ttf or .otf file
        default_font = dpg.add_font("C:/Windows/Fonts/consola.ttf", 20)

    dpg.create_viewport(title="Custom Title", width=600, height=350)

    with dpg.window(tag="Primary Window"):
        # set font of specific widget
        dpg.bind_font(default_font)

        with dpg.tab_bar():
            with dpg.tab(label="BE management"):
                dpg.add_text("Mass-Disenchant Champion Shards accounting for Mastery levels.")
                dpg.add_button(width=500, label="Run", callback=be_mass_disenchant_button)

            with dpg.tab(label="OE management"):
                dpg.add_text("Show skin shards for champions without a skin.")
                dpg.add_button(width=500, label="Run", callback=show_zero_skins_shards_button)

            with dpg.tab(label="Remove Challenges"):
                dpg.add_text("Remove Challenges Tokens.")
                dpg.add_button(width=500, label="Run", callback=remove_challenges_tokens_button)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
