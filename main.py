import os
import customtkinter as ctk
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from Frames import exceptionframe, whitelistframe, loginframe, signupframe, optionsframe, infoframe
from datamanager import Data_Manager
import time
#from packetmanager import Packet_Manager

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        #load extra functionality
        self.data_manager = Data_Manager
        #self.packet_manager = Packet_Manager(self)

        self.conn, self.cur = self.data_manager.connectToDatabase()
        self.default_user, self.default_pass = "user", "pass"
        self.wm_iconphoto(True, tk.PhotoImage(file="Data/Images/firewalliconLight.png"))
        #define what happend on appplication close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        #Check if first time running
        if self.is_first_time_running() is True:
            self.initiate_database(self.default_user, self.default_pass)
            self.set_default_settings()
            self.create_logs_folder()
            self.create_marker_file()

        #Read Settings
        self.settings = self.data_manager.read_settings()
        #Set Settings
        self.set_settings(self.settings)
        self.refresh_logs(self.settings["log auto delete interval"])

        #Initialise GUI components
        self.frame_list = self.initiate_frames()
        self.stack_frames(self.frame_list)
        self.populate_navbars(self.frame_list)
        if self.settings["bypass login"] == "True":
            self.raise_frame("Whitelist_Frame")
        else:
            self.raise_frame("Login_Frame")
    
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
        #self.minsize("659x332") Broken
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
        self.theme = Data_Manager.open_theme(self.current_theme_name)
        self.theme_color = self.theme["CTkButton"]["fg_color"][index]
        self.frame_color_2 = self.theme["CTkFrame"]["top_fg_color"][index]
        self.frame_color = self.theme["CTkFrame"]["fg_color"][index]

    def on_setting_change(self):
        for frame in self.frame_list:
            frame.destroy()

        self.data_manager.update_setting("fullscreen", str(self.attributes("-fullscreen")))
        self.settings = Data_Manager.read_settings()
        self.set_settings(self.settings)

        self.frame_list = self.initiate_frames()
        self.stack_frames(self.frame_list)
        self.populate_navbars(self.frame_list)
        self.raise_frame("Options_Frame")

    def initiate_frames(self):
        self.login_frame = loginframe.Login_Frame(self, has_navbar=False)
        self.signup_frame = signupframe.Signup_Frame(self, has_navbar=False)
        self.whitelist_frame = whitelistframe.Whitelist_Frame(self,has_navbar=True, navbar_name = "Whitelists")
        self.rule_frame = exceptionframe.Exception_Frame(self, has_navbar=True, navbar_name="Exceptions")
        self.info_frame = infoframe.Info_Frame(self, has_navbar=True, navbar_name="Information")
        self.options_frame = optionsframe.Options_Frame(self, has_navbar=True, navbar_name = "Options")
        return[self.login_frame, self.signup_frame, self.whitelist_frame, self.rule_frame, self.options_frame, self.info_frame]
    
    def populate_navbars(self, frame_list):
        for frame in frame_list:
            if frame.has_navbar is True:
                frame.navbar.populate_navbar(frame, self, frame_list)

    def stack_frames(self, frame_list):
        for frame in frame_list:
            frame.place(relx=0.5, rely=0.5, anchor="center" ,relwidth = 1, relheight = 1)

    def raise_frame(self, frame_string):
        for frame in self.frame_list:
            if frame.__class__.__name__ == frame_string:
                frame.tkraise()
    
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
        self.data_manager.createDatabase(self.conn, self.cur)
        self.data_manager.insertUser(self.conn, self.cur, default_user, default_pass)

    def refresh_logs(self, deletion_interval):
        log_directory = os.fsencode("Data/Logs")
        current_time = time.time()

        if deletion_interval != "Never":
            deletion_interval_seconds = self.time_to_seconds(deletion_interval)
            for file in os.listdir(log_directory):
                filepath = "Data/Logs/"+os.fsdecode(file)
                time_created = os.path.getctime(filepath)
                time_difference = current_time - time_created
                if time_difference - deletion_interval_seconds > 0:
                    os.remove(filepath)
        self.after(3600000, self.refresh_logs)
    
    def time_to_seconds(self, deletion_interval):
        match deletion_interval:
            case "1 Day":
                return 86400
            case "5 Days":
                return 432000
            case "1 Week":
                return 604800
            case "2 Weeks":
                return 1.2096e+6
            case "1 Month":
                return 2.6298e+6
            case "3 Months":
                return 7.889399e+6
            case "6 months":
                return 1.57788e+7
            case "1 Year":
                return 3.15576e+7

    def on_closing(self):
       if (CTkMessagebox(title="Quit", message="Do you want to quit?, packet filtering will be disabled", option_1="No", option_2="yes")).get() == "yes":
           self.data_manager.update_setting("geometry", str(self.winfo_width())+"x"+str(self.winfo_height()))
           self.data_manager.update_setting("fullscreen", str(self.attributes("-fullscreen")))
           self.destroy()
        
if __name__ == "__main__" :
    app = Application()
    app.mainloop()
    