from Frames.custom_components import Container, Custom_Frame, Whitelist_Container, Sidebar

class Whitelist_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, column = 1, row = 1, color="transparent", sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.port_whitelist_container = Whitelist_Container(self.main_container, App, name="Port", description="whitelist and blacklist different ports, When adding the rule add via the port number instead of the name.", pady=App.uniform_padding_y)
        self.protocol_whitelist_container = Whitelist_Container(self.main_container, App, name="Protocol", description="whitelist and blacklist different transport layer Protocols such as, ICMP, UDP or TCP", pady=App.uniform_padding_y)
        self.application_whitelist_container = Whitelist_Container(self.main_container, App, name="Application", description="FIlter out Applications, These can be similar to the port filters althouogh it can attempt to make guesses for various layer seven applications as well. This feature is experimental and may not work as expected", pady=App.uniform_padding_y)
        self.address_whitelist_container = Whitelist_Container(self.main_container, App, name="Address", description="whitelist and blacklist different IP addresses, enter the IPv4 or IPv6 address to be whitlisted or blacklisted.", pady=App.uniform_padding_y)
        
        self.subcontainers = [self.address_whitelist_container, self.application_whitelist_container, self.port_whitelist_container, self.protocol_whitelist_container]

        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Whitelists", subcontainers=self.subcontainers, loadedcontainer=self.address_whitelist_container)

    def populate_containers(self, App):
       pass