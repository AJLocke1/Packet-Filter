import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from Frames import filterframe, loginframe, signupframe, optionsframe, logframe
import os
from datamanager import Data_Manager

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        #load extra functionality
        self.data_manager = Data_Manager
        self.conn, self.cur = self.data_manager.connectToDatabase()
        self.default_user, self.default_pass = "user", "pass"
        #define what happend on appplication close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #Read Settings
        self.settings = Data_Manager.read_settings()
        #Set Settings
        self.set_settings(self.settings)
        #Check if first time running
        if self.is_first_time_running() is True:
            self.initiate_database(self.default_user, self.default_pass)
            self.create_marker_file()

        #Initialise GUI components
        self.frame_list = self.initiate_frames()
        self.stack_frames(self.frame_list)
        self.populate_navbars(self.frame_list)
        if self.settings["bypass login"] == "True":
            self.raise_frame("Filter_Frame")
        else:
            self.raise_frame("Login_Frame")
    
    def set_settings(self, settings):
        self.geometry(settings["geometry"])
        self.attributes("-fullscreen", settings["fullscreen"])
        self.title(settings["application name"])
        self.bypass_login_string = settings["bypass login"]
        self.widget_scaling_value = settings["widget scaling"]
        self.enable_ML_string = settings["enable machine learning"]
        self.enable_filter_string = settings["enable filtering"]
        self.machine_learning_priority = settings["machine learning priority"]
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

        self.settings = Data_Manager.read_settings()
        self.set_settings(self.settings)

        self.frame_list = self.initiate_frames()
        self.stack_frames(self.frame_list)
        self.populate_navbars(self.frame_list)
        self.raise_frame("Options_Frame")

    def initiate_frames(self):
        self.login_frame = loginframe.Login_Frame(self, has_navbar=False)
        self.signup_frame = signupframe.Signup_Frame(self, has_navbar=False)
        self.filter_frame = filterframe.Filter_Frame(self,has_navbar=True, navbar_name = "Filters")
        self.log_frame = logframe.Log_Frame(self, has_navbar=True, navbar_name="Statistics")
        self.options_frame = optionsframe.Options_Frame(self, has_navbar=True, navbar_name = "Options")
        return[self.login_frame, self.signup_frame, self.filter_frame, self.log_frame, self.options_frame]
    
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
    
    def create_marker_file(self):
        marker_path = "Data/marker_file.txt"
        with open(marker_path, "w") as marker_file:
            marker_file.write("This file marks that the application has been run.")

    def initiate_database(self, default_user, default_pass):
        self.data_manager.createDatabase(self.conn, self.cur)
        self.data_manager.insertUser(self.conn, self.cur, default_user, default_pass)

    def on_closing(self):
       if (CTkMessagebox(title="Quit", message="Do you want to quit?, packet filtering will be disabled", option_1="No", option_2="yes")).get() == "yes":
           self.data_manager.update_setting("geometry", str(self.winfo_width())+"x"+str(self.winfo_height()))
           self.data_manager.update_setting("fullscreen", str(self.attributes("-fullscreen")))
           self.destroy()
        
if __name__ == "__main__" :
    app = Application()
    app.mainloop()