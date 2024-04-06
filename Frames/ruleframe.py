from Frames.custom_components import Container, Custom_Frame, Scrolable_Container
import customtkinter as ctk

class Rule_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, sticky="nsew", color=App.frame_color_2, padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=0)
        self.main_container.grid_columnconfigure(0, weight = 1)
        self.main_container.grid_rowconfigure(1, weight = 1)

        self.top_container = Container(self.main_container, App, isCentered=False, sticky="nsew", color=App.frame_color, padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0)
        self.top_container.grid_columnconfigure(0, weight = 1)
        self.body_container = Scrolable_Container(self.main_container, App, isCentered=False, sticky="nsew", color=App.frame_color, padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=0)
        self.body_container.grid_columnconfigure(0, weight = 1)


    def populate_containers(self, App):
        self.label = ctk.CTkLabel(self.top_container, text="Rules")
        self.label.grid(row=0, column=0)

        self.label = ctk.CTkLabel(self.body_container, text="Content")
        self.label.grid(row=0, column=0)