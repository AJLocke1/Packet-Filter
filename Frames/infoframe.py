from Frames.custom_components import Container, Custom_Frame, Scrolable_Container, Sidebar, Info_Pannel, Log
import customtkinter as ctk
from PIL import Image
import os
import nmap
import subprocess
import re
import ipaddress
class Info_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)
        self.main_container.grid_columnconfigure(0, weight = 1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.log_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Logs")
        self.log_container.grid_columnconfigure(0, weight = 1)
        self.log_container.grid_rowconfigure(4, weight=1)

        self.network_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Network")
        self.network_container.grid_columnconfigure(0, weight = 1)

        self.information_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Information")
        self.information_container.grid_columnconfigure(0, weight = 1)

        self.subcontainers = [self.information_container, self.log_container, self.network_container]

        #Subcontainers for the information container
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

        self.filter_info_pannel = Info_Pannel(self.information_container, App, column = 0, row = 1, title="How the Filter Works", body = self.filter_info_pannel_contents)

        #Subcontainers for the log container
        self.log_table = Scrolable_Container(self.log_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=2, column=0)
        self.log_display = Container(self.log_container, App, isCentered=False, color=App.frame_color, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=5, column=0)

        #Currently using a windows command for testing
        self.ip_display = Info_Pannel(self.network_container, App, title="IP Address", body=self.get_ip(), row=0, column = 0)
        self.subnet_display = Info_Pannel(self.network_container, App, title="Subnet Mask", body=self.get_subnet(), row=1, column = 0)
        self.subnet_addresses_display = Info_Pannel(self.network_container, App, title="Subnet Addresses", body=self.get_subnet_addresses(self.ip_display.body.cget("text"), self.subnet_display.body.cget("text")), row=2, column = 0)
        self.scan_display = Container(self.network_container, App, isCentered=False, row=3, column=0, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)


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

        log_directory = os.fsencode("Data/Logs")
        for file in os.listdir(log_directory):
                log_name = os.fsdecode(file)
                self.log = Log(self.log_table, App, log_name, self.log_display)

        self.scan_display_title = ctk.CTkLabel(self.scan_display, text="Scan the IP Addresses To Locate Networkm Components", font=("", 20))
        self.scan_display_title.grid(row=0, column=0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

    def get_ip(self): #MAC and Linux Versions here for testing only
        try:
            ip_regex = r'inet (\d+\.\d+\.\d+\.\d+)'
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            output = result.stdout

            # Find the first match of IP address
            match = re.search(ip_regex, output)
            if match:
                ip_address = match.group(1)
                return ip_address
            else:
                return None
        except Exception as e:
            ip_regex = r'inet (\d+\.\d+\.\d+\.\d+)'
            result = subprocess.run(['ifconfig', 'en0'], capture_output=True, text=True)
            output = result.stdout

            # Find the first match of IP address
            match = re.search(ip_regex, output)
            if match:
                ip_address = match.group(1)
                return ip_address
            else:
                return None

    def get_subnet(self): #MAC and Linux Versions here for testing only
        try:
            subnet_regex = r'netmask (\S+)'
            result = subprocess.run(['ip', 'addr', 'show'], capture_output=True, text=True)
            output = result.stdout

            # Find the first match of subnet mask
            match = re.search(subnet_regex, output)
            if match:
                subnet_mask = match.group(1)
                return subnet_mask
            else:
                return None
        except Exception as e:
            subnet_regex = r'inet \d+\.\d+\.\d+\.\d+ netmask (\S+)'
            result = subprocess.run(['ifconfig', 'en0'], capture_output=True, text=True)
            output = result.stdout

            # Find the first match of subnet mask
            match = re.search(subnet_regex, output)
            if match:
                subnet_mask_str = match.group(1)
                subnet_mask_int = int(subnet_mask_str, 16)  # Convert hexadecimal string to integer
                subnet_mask = ipaddress.IPv4Address(subnet_mask_int)  # Convert integer to IPv4Address object
                return str(subnet_mask)
            else:
                print(output)
                return None
            
    def get_subnet_addresses(self, ip, subnet):
        network = ipaddress.IPv4Network(ip + '/' + subnet, strict=False)
        subnet_addresses = str(next(network.hosts())) + " To " + str(next(reversed(list(network.hosts()))))
        return subnet_addresses
        

