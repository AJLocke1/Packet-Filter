from Frames.custom_components import Container, Custom_Frame, Scrolable_Container, Sidebar, Info_Pannel, Log, Result
import customtkinter as ctk
from PIL import Image
import os
import nmap
import subprocess
import re
import ipaddress
import threading


class Utilities_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)
        self.main_container.grid_columnconfigure(0, weight = 1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.network_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Network")
        self.network_container.grid_columnconfigure(0, weight = 1)

        self.log_container = Scrolable_Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", row=0, column=0, name="Logs")
        self.log_container.grid_columnconfigure(0, weight = 1)
        self.log_container.grid_rowconfigure(4, weight=1)

        self.subcontainers = [self.log_container, self.network_container]

        #Subcontainers for the log container
        self.log_table = Scrolable_Container(self.log_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=2, column=0)
        self.log_display = Container(self.log_container, App, isCentered=False, color=App.frame_color, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=5, column=0)

        #Currently using a windows command for testing
        self.ip_display = Info_Pannel(self.network_container, App, title="IP Address", body=self.get_ip(), row=0, column = 0)
        self.subnet_display = Info_Pannel(self.network_container, App, title="Subnet Mask", body=self.get_subnet(), row=1, column = 0)
        self.subnet_addresses_display = Info_Pannel(self.network_container, App, title="Subnet Addresses", body=self.get_first_and_last_subnet_addresses(self.ip_display.body.cget("text"), self.subnet_display.body.cget("text")), row=2, column = 0)
        self.scan_display = Container(self.network_container, App, isCentered=False, row=3, column=0, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)


        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Utilities", subcontainers=self.subcontainers, loadedcontainer=self.log_container)

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

        self.scan_display_head = Container(self.scan_display, App, isCentered=False, row=0, column = 0, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.scan_display_title = ctk.CTkLabel(self.scan_display_head, text="Scan the Subnet to Locate Network Components", font=("", 20))
        self.scan_display_title.grid(row=0, column=0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w")

        self.scan_button = ctk.CTkButton(self.scan_display_head, text="Scan", command=lambda: self.scan_ip_range(self.get_subnet_hosts(self.ip_display.body.cget("text"), self.subnet_display.body.cget("text")), App))
        self.scan_button.grid(row=0, column=1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.scan_display_description = ctk.CTkLabel(self.scan_display_head, text="When the scan button is clicked all ip addresses within the shown subnet are scanned to check for online network devices. On larger subnets this may take some time.", anchor="w")
        self.scan_display_description.grid(row =1, column=0, columnspan=2, sticky="we")
        self.scan_display_description.bind('<Configure>', lambda event: self.update_wraplength(self.scan_display_head))

        self.scan_status_label = ctk.CTkLabel(self.scan_display_head, text="Scanning", text_color="green")
        self.scan_status_label.grid(row=2, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        self.scan_status_label.grid_remove()

        self.display = Container(self.scan_display, App, isCentered=False, row=1, column=0, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y)
        
    def update_wraplength(self, master):
        self.scan_display_description.update_idletasks()
        self.scan_display_description.configure(wraplength=master.master.winfo_width() - 100)

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
        except Exception:
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
        except Exception:
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
    
    def get_subnet_hosts(self, ip, subnet):
        return ipaddress.IPv4Network(ip + '/' + subnet, strict=False)
            
    def get_first_and_last_subnet_addresses(self, ip, subnet):
        network = self.get_subnet_hosts(ip, subnet)
        subnet_addresses = str(next(network.hosts())) + " To " + str(next(reversed(list(network.hosts()))))
        return subnet_addresses
     
    def scan_ip_range(self, hosts, App):
        self.scan_status_label.grid()

        for widget in self.display.winfo_children():
            widget.destroy()

        scanner_master = ScannerMaster(hosts, App)
        scanner_master.start()

    def display_scan_results(self, results, App):
        for result in results:
            self.display.result = Result(self.display, App, result[0] ,result[1])
            self.display.result.pack(padx = App.uniform_padding_x, pady= App.uniform_padding_y, anchor="w")
        self.scan_status_label.grid_remove()

class ScannerMaster(threading.Thread):
    def __init__(self, hosts, App) :
        super().__init__()
        self.results = {}
        self.scanner_threads = []
        self.hosts = hosts
        self.app = App

    def run(self):
        for host in self.hosts:
            scanner_thread = ScannerThread(host)
            scanner_thread.start()
            self.scanner_threads.append(scanner_thread)

        for scanner_thread in self.scanner_threads:
            scanner_thread.join()

        self.results = [thread.result for thread in self.scanner_threads if thread.result is not None]
        print(self.results)
        self.app.utilities_frame.display_scan_results(self.results, self.app)

class ScannerThread(threading.Thread):
    def __init__(self, host):
        super().__init__()
        self.host = host
        self.result = None

    def run(self):
        scanner = nmap.PortScanner()
        host_str = str(self.host)

        timer = threading.Timer(240, self.timeout)
        timer.start()
                            
        try:
            scan_result = scanner.scan(hosts=host_str, arguments='-O')
            if "osmatch" in scan_result["scan"][host_str]: 
                if len(scan_result["scan"][host_str]["osmatch"]) > 0:
                    os_match = scan_result["scan"][host_str]["osmatch"][0]
                else:
                    os_match = scan_result["scan"][host_str]["osmatch"]
            print(os_match)
            name = os_match["name"] if os_match["name"] is not None else "Unkown Name"
            self.result = [host_str, name]
            print(self.result)
        except Exception as e:
            pass
        finally:
            timer.cancel()

    def timeout(self):
        pass





