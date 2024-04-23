from Frames.custom_components import Container, Custom_Frame, Scrolable_Container, Sidebar, Info_Pannel

class Help_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)
        self.main_container.grid_columnconfigure(0, weight = 1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.filter_types_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Catagories")
        self.filter_types_container.grid_columnconfigure(0, weight = 1)

        self.filter_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Rulesets")
        self.filter_container.grid_columnconfigure(0, weight = 1)

        self.subcontainers = [self.filter_container, self.filter_types_container]

    def populate_containers(self, App):

        self.filter_info_pannel_contents = """The packet filter operates using four main components to construct a ruleset:

1. Whitelists:
Whitelists define the default behavior for filtering packets based on their general characteristics. For instance, you can configure whitelists to block all packets arriving on port 22.

2. Exceptions:
Exceptions allow for specific conditions to overwrite the default behavior set by whitelists. For example, you can create exceptions to allow packets on port 22 only if they also match the MAC address of the user's laptop. While still having a balcklist on all port 22 traffic.

3. Whitelist Strictness Values:
These values determine the default behavior when a value is not specified in one of the whitelists. For instance, if a packet on port 80 is filtered but not specified to be whitelisted or blacklisted, the behavior depends on the whitelist strictness setting. If set to strict, it will be blocked; if set to unstrict, it will be allowed through.

4. Machine Learning Algorithms:
Machine learning algorithms complement user-defined rules and provide additional protection against oversights. You can configure these algorithms to operate at different priorities, ranging from low to high, or disable them entirely.
        """

        self.filter_info_pannel = Info_Pannel(self.filter_container, App, column = 0, row = 1, title="How the Filter Works", body = self.filter_info_pannel_contents)

        self.filter_catagory_info_pannel_contents = """The packet filter allows for filtering based on 5 catagories:

1. IP Addresses:
IP Addresses are the logical address of a networked computer device. They are often dynamically assigned to a device by the network routers DHCP but can also be statically assigned manually.

2. MAC Adresses:
MAC Adresses are the physical address of a computer device. They corrispond to a devices specific network interface.

3. Ports:
Ports are part of the transport layer of the network communication stack. They are used to keep track of which type of service is being used e.g port 80 for web services. alongside what logical port the communication should be received by.

4. Protocols:
Protocols define the transmition method of the packets on the transport layer. E.g TCP or UDP. Some protocols are only used by specific functionality such as ICMP.

5. Application:
Applications are the highest level of information on the network com,munication stack. These corrispond to which programs the user is using to generate internet traffic. e.g Youtube.
        """
        self.filter_catagory_info_pannel = Info_Pannel(self.filter_types_container, App, column=0, row=2, title="Filtering Catagories", body = self.filter_catagory_info_pannel_contents)

        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Help", subcontainers=self.subcontainers, loadedcontainer=self.filter_container)