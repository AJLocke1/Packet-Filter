from Frames.custom_components import Container, Scrolable_Container, Custom_Frame
import customtkinter as ctk

class Log_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
    def initialise_containers(self, App):
        self.container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.label = ctk.CTkLabel(self.container, text="Statistics")
        self.label.grid(row=0, column=0)