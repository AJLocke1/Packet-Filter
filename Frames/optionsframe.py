from Frames.custom_components import Container, Scrolable_Container, Custom_Frame, Sidebar
import customtkinter as ctk
from os import listdir
from os.path import isfile, join

class Options_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Scrolable_Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)

        self.UI_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="UI")

        self.change_theme_option_container = Container(self.UI_option_container, App, isCentered=False, color = App.frame_color, padx=App.uniform_padding_x, pady=App.uniform_padding_y, row = 0, column = 0)
        self.change_appearance_option_container = Container(self.UI_option_container, App, isCentered=False, color = App.frame_color, padx=App.uniform_padding_x, pady=App.uniform_padding_y, row = 0, column = 1)

        self.subcontainers = [self.UI_option_container]
        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Options", subcontainers=self.subcontainers, loadedcontainer=self.UI_option_container)

    def populate_containers(self, App):
        self.populate_change_theme_option_container(App, self.change_theme_option_container)
        self.populate_change_appearance_option_container(App, self.change_appearance_option_container)

    def populate_change_theme_option_container(self, App, container):
        self.theme_appearance_label = ctk.CTkLabel(container, text="Change Theme")
        self.theme_appearance_label.grid(row=0, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.theme_dropdown_value = ctk.StringVar(value = App.current_theme_name)
        self.theme_dropdown = ctk.CTkOptionMenu(container, values=[f.split(".", 1)[0] for f in listdir("Data/Themes/") if isfile(join("Data/Themes/", f))], command=lambda value: self.change_theme(App), variable=self.theme_dropdown_value)
        self.theme_dropdown.grid(row=1, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

    def change_theme(self, App):
        value = self.theme_dropdown_value.get()
        App.data_manager.update_setting("theme", value)
        App.on_setting_change()

    def populate_change_appearance_option_container(self, App, container):
        self.theme_appearance_label = ctk.CTkLabel(container, text="Toggle Light and Dark Mode")
        self.theme_appearance_label.grid(row=0, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, columnspan=3)

        self.dark_label = ctk.CTkLabel(container, text="Dark Mode")
        self.dark_label.grid(row=1, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.appearance_mode_radio_value = ctk.StringVar(value = App.appearance_mode_string)
        self.appearance_mode_radio = ctk.CTkSwitch(container, text="Light Mode", command= lambda: self.toggle_appearance_mode(App), variable=self.appearance_mode_radio_value, onvalue="Light", offvalue="Dark")
        self.appearance_mode_radio.grid(row = 1, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

    def toggle_appearance_mode(self, App):
        value = self.appearance_mode_radio_value.get()
        App.data_manager.update_setting("appearance mode", value)
        App.on_setting_change()
