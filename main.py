import os
import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox

from datamanager import Data_Manager
from uimanager import UI_Manager
try:
    from packetmanager import Packet_Manager
except ModuleNotFoundError:
    print("Must be run on Linux for filtering functionality")

"""
program needs to be run with root privlige, on linux hardware while connected to the internet for full functionality.
"""
class Application(ctk.CTk):
    """
    The main application class

    The class is responsible for managing the flow of the Application. It is a
    subclass ot the tkinter window class.

    Attributes
    default_user : str
        The default username for loggin into the applicaiton
    defult_pass : str
        The default password for logging into the application
    defult_settings : dict
        The default application settings.
    uniform_padding_x : tuple
        The uniform x padding when creating widgts
    uniform_padding_y : tuple
        The uniform y padding when creating widgets
    data_manager : Data_Manager
        The class responsible for any data manipulation in the application
    packet_manager : Packet_Manager
        The class responsible for any packet filtering in the application
    ui_manager : UI_Manager
        The class responsible for placing and manipulating the UI
    """ 
    def __init__(self):
        super().__init__()
        #Set the default application settings and any non changing settings.
        self.default_user, self.default_pass = "user", "pass"
        self.default_settings = {
                                    "widget scaling": 1,
                                    "theme": "green",
                                    "appearance mode": "Dark",
                                    "fullscreen": "0",
                                    "bypass login": "False",
                                    "enable filtering": "True",
                                    "enable machine learning": "True",
                                    "machine learning priority": "low",
                                    "enable logs": "True",
                                    "log auto delete interval": "Never",
                                    "enable killswitch": "False",
                                    "IP whitelist strictness": "Unstrict",
                                    "MAC whitelist strictness": "Unstrict",
                                    "port whitelist strictness": "Unstrict",
                                    "protocol whitelist strictness": "Unstrict",
                                    "application whitelist strictness": "Unstrict"
                                }
        self.wm_iconphoto(True, tk.PhotoImage(file="Data/Images/firewalliconLight.png"))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.title("Packet Filter")
        self.minsize(1000,400)
        self.uniform_padding_x = (5,5)
        self.uniform_padding_y = (5,5)

        #load managers
        self.data_manager = self.load_datamanager()
        self.packet_manager = self.load_packetmanager()
        self.ui_manager = self.load_uimanager()
        
        #Check if first time running
        if self.is_first_time_running() is True:
            self.data_manager.initiate_database(self.default_user, self.default_pass)
            self.set_default_settings()
            self.create_marker_file()

        #set any cahngeable settings
        self.settings = self.data_manager.read_settings()
        self.set_settings(self.settings)

        #Start Aplication Processes
        self.data_manager.refresh_logs(self, self.settings["log auto delete interval"])
        self.ui_manager.start_ui()

    def load_datamanager(self):
        try:
            return Data_Manager(self)
        except Exception as e:
            print("Error Loading Data Manager", e)

    def load_packetmanager(self):
        try:
            return Packet_Manager(self)
        except Exception as e:
            print("Error Loading Packet Manager", e)

    def load_uimanager(self):
        try:
            return UI_Manager(self)
        except Exception as e:
            print("Error Loading UI Manager", e)
    
    def set_settings(self, settings):
        self.geometry(settings["geometry"])
        self.attributes("-fullscreen", settings["fullscreen"])
        try:
            ctk.set_widget_scaling(float(settings["widget scaling"]))
        except Exception:
            pass #Some widgets error when being scaled
        ctk.set_appearance_mode(settings["appearance mode"])
        self.set_color_theme(settings["theme"], settings["appearance mode"])
 
    def set_default_settings(self):
        for setting in self.default_settings:
            self.data_manager.update_setting(setting, setting.value())

    def set_color_theme(self, theme, appearance_mode_string):
        if appearance_mode_string == "Dark":
            index=1
        else:
            index=0
        ctk.set_default_color_theme("Data/Themes/"+theme+".json")
        self.theme = self.data_manager.open_theme(theme)
        self.theme_color = self.theme["CTkButton"]["fg_color"][index]
        self.frame_color_2 = self.theme["CTkFrame"]["top_fg_color"][index]
        self.frame_color = self.theme["CTkFrame"]["fg_color"][index]
    
    def is_first_time_running(self):
        marker_path = "Data/marker_file.txt"  # Define the path for the marker file
        # Check if the marker file exists
        if os.path.exists(marker_path):
            return False  # Application has been run before
        else:
            return True
    
    def create_marker_file(self):
        marker_path = "Data/marker_file.txt"
        with open(marker_path, "w") as marker_file:
            marker_file.write("This file marks that the application has been run.")

    def on_closing(self):
       if (CTkMessagebox(title="Quit", message="Do you want to quit?, packet filtering will be disabled", option_1="No", option_2="yes")).get() == "yes":
           self.data_manager.update_setting("geometry", str(self.winfo_width())+"x"+str(self.winfo_height()))
           self.data_manager.update_setting("fullscreen", str(self.attributes("-fullscreen")))
           #self.packet_manager.end_pcket_capture()
           self.destroy()
        
if __name__ == "__main__" :
    app = Application()
    app.mainloop()
    