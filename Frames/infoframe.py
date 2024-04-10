from Frames.custom_components import Container, Custom_Frame, Scrolable_Container, Sidebar, Info_Pannel
import customtkinter as ctk

class Info_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Scrolable_Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)
        self.grid_columnconfigure(0, weight = 1)

        self.log_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Logs")
        self.log_container.grid_columnconfigure(0, weight = 1)
        self.information_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Information")
        self.information_container.grid_columnconfigure(0, weight = 1)
        
        self.subcontainers = [self.information_container, self.log_container]

        self.filter_info_pannel = Info_Pannel(self.information_container, App, column = 0, row = 1, title="FIltering Information", body = "Text")

        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Information", subcontainers=self.subcontainers, loadedcontainer=self.information_container)

    def populate_containers(self, App):
        self.label = ctk.CTkLabel(self.information_container, text="Information")
        self.label.grid(row=0, column=0)