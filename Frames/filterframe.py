from Frames.custom_components import Container, Scrolable_Container, Custom_Frame, Sidebar_Button, Filter_Container, Sidebar
import customtkinter as ctk

class Filter_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, column = 1, row = 1, color="transparent", sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.filter_container_2 = Filter_Container(self.main_container, App, filter_name="Port", filter_description="whitelist and blacklist different ports, When adding the rule add via the port number instead of the name.", pady=App.uniform_padding_y)
        self.filter_container_3 = Filter_Container(self.main_container, App, filter_name="Protocol", filter_description="whitelist and blacklist different Protocols, Omly availible options are ICMP, UDP, and TCP. This section main use is for blocking or allowing ICMP traffic.", pady=App.uniform_padding_y)
        self.filter_container_5 = Filter_Container(self.main_container, App, filter_name="Compound Rules", filter_description="Define compound rules based on combinations of ports, IP Addresses and Protocols", pady=App.uniform_padding_y)
        self.filter_container_1 = Filter_Container(self.main_container, App, filter_name="Address", filter_description="whitelist and blacklist different IP addresses, enter the IPv4 or IPv6 address to be whitlisted or blacklisted.", pady=App.uniform_padding_y)
        
        self.subcontainers = [self.filter_container_1, self.filter_container_2, self.filter_container_3, self.filter_container_5]

        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Filters", subcontainers=self.subcontainers, loadedcontainer=self.filter_container_1)

    def populate_containers(self, App):
       pass