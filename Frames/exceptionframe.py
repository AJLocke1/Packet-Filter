from Frames.custom_components import Container, Custom_Frame, Scrolable_Container, Exception_Creation_Window
import customtkinter as ctk
from PIL import Image

class Exception_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):

        self.exception_creation_window = None
        self.image = ctk.CTkImage(light_image=Image.open("Data/Images/PlusSymbol.png"),dark_image=Image.open("Data/Images/PlusSymbolLight.png"))

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
        self.label = ctk.CTkLabel(self.top_container, text="Create Exceptions")
        self.label.grid(row=0, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.add_exception_button = ctk.CTkButton(self.top_container, text="", width=30, image=self.image, command = lambda: self.add_exception(App))
        self.add_exception_button.grid(row=0, column = 1, sticky="e", padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label2 = ctk.CTkLabel(self.top_container, text="Create Exceptions. These have priority over whitelists.")
        self.label2.grid(row=1, column = 0, sticky="we", columnspan = 2, padx=[5,5], pady = [5,5])
        self.label2.bind('<Configure>', lambda event: self.update_wraplength(self))

    def update_wraplength(self, master):
        self.label2.update_idletasks()
        self.label2.configure(wraplength=master.master.winfo_width() - 100)

    def add_exception(self, App):
        if self.exception_creation_window is None or not self.exception_creation_window.winfo_exists():
            self.exception_creation_window = Exception_Creation_Window(self, App)  # create window if its None or destroyed
        else:
            self.exception_creation_window.focus() 