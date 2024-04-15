from Frames.custom_components import Container, Custom_Frame, Scrolable_Container, Sidebar, Info_Pannel, Log
import customtkinter as ctk
from PIL import Image
import os

class Info_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Scrolable_Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)
        self.main_container.grid_columnconfigure(0, weight = 1)

        self.log_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Logs")
        self.log_container.grid_columnconfigure(0, weight = 2)
        self.information_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Information")
        self.information_container.grid_columnconfigure(0, weight = 1)
        
        self.subcontainers = [self.information_container, self.log_container]

        #Subcontainers for the information container
        self.filter_info_pannel = Info_Pannel(self.information_container, App, column = 0, row = 1, title="FIltering Information", body = "Text")

        #Subcontainers for the log container
        self.log_table = Scrolable_Container(self.log_container, App, isCentered=False, color=App.frame_color, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=2, column=0)
        self.log_display = Scrolable_Container(self.log_container, App, isCentered=False, color=App.frame_color, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=5, column=0)

        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Information", subcontainers=self.subcontainers, loadedcontainer=self.information_container)

    def populate_containers(self, App):

        self.log_title = ctk.CTkLabel(self.log_container, text="Select A Log", font=("", 20))
        self.log_title.grid(row=0, column = 0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(250,10))
        self.log_seperator = ctk.CTkLabel(self.log_container, text="", image=self.seperator_image)
        self.log_seperator.grid(row=1, column=0, sticky="w")

        self.log_title_2 = ctk.CTkLabel(self.log_container, text="Display Pannel", font=("", 20))
        self.log_title_2.grid(row=3, column = 0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

        self.log_seperator_2 = ctk.CTkLabel(self.log_container, text="", image=self.seperator_image)
        self.log_seperator_2.grid(row=4, column=0, sticky="w")

        log_directory = os.fsencode("Logs")
        for file in os.listdir(log_directory):
                log_name = os.fsdecode(file)
                self.log = Log(self.log_table, App, log_name, self.log_display)