from Frames.custom_components import Container, Scrolable_Container, Cutsom_Frame, Sidebar_Button
import customtkinter as ctk

class Filter_Frame(Cutsom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, column = 1, row = 1, color="transparent", sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.filter_container_1 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="green")
        self.filter_container_2 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="orange")
        self.filter_container_3 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="blue")
        self.filter_container_4 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="red")
        self.filter_container_5 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="pink")
        self.filter_container_6 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="purple")
        self.filter_container_7 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="yellow")
        self.filter_container_8 = Scrolable_Container(self.main_container, App, isCentered=False, column = 0, row = 0, sticky="nsew", color="brown")

        self.subcontainers = [self.filter_container_1, self.filter_container_2, self.filter_container_3, self.filter_container_4, self.filter_container_5, self.filter_container_6, self.filter_container_7, self.filter_container_8]

        self.sidebar_container = Container(self, App, isCentered=False, column = 0, row = 1, color="transparent", sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.sidebar_container.grid_columnconfigure(0, weight=1)

    def populate_containers(self, App):
        self.populate_sidebar_container(App, self.subcontainers)

    def populate_sidebar_container(self, App, subcontainers):
        label = ctk.CTkLabel(self.sidebar_container, text="Filters")
        label.grid(row=0, column =0)
        for i, subcontainer in enumerate(subcontainers):
            button = Sidebar_Button(self.sidebar_container, App, text=f"Filter {i+1}", command=lambda c=subcontainer: self.sidebar_container.raise_subcontainer(c))
            button.grid(row=i+1, column=0, sticky="ew")