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
    def __init__(self):
        super().__init__()

        #Set the default application settings
        self.default_user, self.default_pass = "user", "pass"
        self.wm_iconphoto(True, tk.PhotoImage(file="Data/Images/firewalliconLight.png"))
        #define what happend on appplication close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        #load managers
        self.load_managers()

        #set settings
        self.settings = self.data_manager.read_settings()
        self.set_settings(self.settings)
        self.data_manager.refresh_logs(self, self.settings["log auto delete interval"])
        
        #Check if first time running
        if self.is_first_time_running() is True:
            self.initiate_database(self.default_user, self.default_pass)
            self.set_default_settings()
            self.create_logs_folder()
            self.create_marker_file()

        #start UI
        self.ui_manager.start_ui()

    def load_managers(self):
        try:
            self.data_manager = Data_Manager(self)
        except Exception as e:
            print("Error Loading Data Manager", e)
        try:
            self.packet_manager = Packet_Manager(self)
        except Exception as e:
            print("Error Loading Packet Manager", e)
        try:
            self.ui_manager = UI_Manager(self)
        except Exception as e:
            print("Error Loading UI Manager", e) 
    
    def set_default_settings(self):
        self.data_manager.update_setting("widget scaling", 1.0)
        self.data_manager.update_setting("theme", "green")
        self.data_manager.update_setting("appearance mode", "Dark")
        self.data_manager.update_setting("fullscreen", "0")
        self.data_manager.update_setting("bypass login", "False")
        self.data_manager.update_setting("enable filtering", "True")
        self.data_manager.update_setting("enable machine learning", "True")
        self.data_manager.update_setting("machine learning priority", "low")
        self.data_manager.update_setting("enable logs", "True")
        self.data_manager.update_setting("log auto delete interval", "Never")
        self.data_manager.update_setting("enable killswitch", "False")
        self.data_manager.update_setting("IP whitelist strictness", "Unstrict")
        self.data_manager.update_setting("MAC whitelist strictness", "Unstrict")
        self.data_manager.update_setting("port whitelist strictness", "Unstrict")
        self.data_manager.update_setting("protocol whitelist strictness", "Unstrict")
        self.data_manager.update_setting("application whitelist strictness", "Unstrict")

    def set_settings(self, settings):
        self.minsize(1000,400) 
        self.geometry(settings["geometry"])
        self.attributes("-fullscreen", settings["fullscreen"])
        self.title(settings["application name"])
        self.bypass_login_string = settings["bypass login"]
        self.widget_scaling_value = settings["widget scaling"]
        self.enable_ML_string = settings["enable machine learning"]
        self.enable_filter_string = settings["enable filtering"]
        self.machine_learning_priority = settings["machine learning priority"]
        self.enable_logs_string = settings["enable logs"]
        self.log_auto_delete_interval = settings["log auto delete interval"]
        self.enable_killswitch_string = settings["enable killswitch"]
        self.IP_whitelist_strictness_string = settings["IP whitelist strictness"]
        self.MAC_whitelist_strictness_string = settings["MAC whitelist strictness"]
        self.port_whitelist_strictness_string = settings["port whitelist strictness"]
        self.protocol_whitelist_strictness_string = settings["protocol whitelist strictness"]
        self.application_whitelist_strictness_string = settings["application whitelist strictness"]

        try:
            ctk.set_widget_scaling(self.widget_scaling_value)
        except Exception as e:
            print(e)
        self.uniform_padding_x = (5,5)
        self.uniform_padding_y = (5,5)
        self.current_theme_name = settings["theme"]
        self.appearance_mode_string = settings["appearance mode"]
        ctk.set_appearance_mode(self.appearance_mode_string) 
        self.set_color_theme(self.current_theme_name, self.appearance_mode_string)
    
    def set_color_theme(self, theme, appearance_mode_string):
        if appearance_mode_string == "Dark":
            index=1
        else:
            index=0
        ctk.set_default_color_theme("Data/Themes/"+theme+".json")
        self.theme = self.data_manager.open_theme(self.current_theme_name)
        self.theme_color = self.theme["CTkButton"]["fg_color"][index]
        self.frame_color_2 = self.theme["CTkFrame"]["top_fg_color"][index]
        self.frame_color = self.theme["CTkFrame"]["fg_color"][index]

    def on_setting_change(self):
        for frame in self.frame_list:
            frame.destroy()

        self.data_manager.update_setting("fullscreen", str(self.attributes("-fullscreen")))
        self.settings = self.data_manager.read_settings()
        self.set_settings(self.settings)

        self.frame_list = self.ui_manager.initiate_frames()
        self.ui_manager.stack_frames()
        self.ui_manager.populate_navbars()
        self.ui_manager.raise_frame("Settings_Frame")
    
    def is_first_time_running(self):
        marker_path = "Data/marker_file.txt"  # Define the path for the marker file
        # Check if the marker file exists
        if os.path.exists(marker_path):
            return False  # Application has been run before
        else:
            return True
        
    def create_logs_folder(self):
        os.makedirs("Data/Logs")
    
    def create_marker_file(self):
        marker_path = "Data/marker_file.txt"
        with open(marker_path, "w") as marker_file:
            marker_file.write("This file marks that the application has been run.")

    def initiate_database(self, default_user, default_pass):
        self.data_manager.create_database(self.conn, self.cur)
        self.data_manager.insert_user(self.conn, self.cur, default_user, default_pass)

    def on_closing(self):
       if (CTkMessagebox(title="Quit", message="Do you want to quit?, packet filtering will be disabled", option_1="No", option_2="yes")).get() == "yes":
           self.data_manager.update_setting("geometry", str(self.winfo_width())+"x"+str(self.winfo_height()))
           self.data_manager.update_setting("fullscreen", str(self.attributes("-fullscreen")))
           self.destroy()
        
if __name__ == "__main__" :
    app = Application()
    app.mainloop()
    