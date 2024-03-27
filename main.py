import customtkinter as ctk
from Frames import filterframe, homeframe, loginframe, signupframe, optionsframe, logframe
import os
from datamanager import Data_Manager

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        #load extra functionality
        self.data_manager = Data_Manager
        #Set Default Settings
        self.geometry("800x550")
        self.title("Packet Filter")
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("green")
        ctk.set_widget_scaling(1.2)
        self.uniform_padding_x = (5,5)
        self.uniform_padding_y = (5,5)
        self.current_theme_name = "green"
        self.theme = Data_Manager.open_theme(self.current_theme_name)   
        self.theme_color = self.theme["CTkButton"]["fg_color"][1]
        self.frame_color_2 = self.theme["CTkFrame"]["top_fg_color"][1]
        self.frame_color = self.theme["CTkFrame"]["fg_color"][1]
        self.conn, self.cur = self.data_manager.connectToDatabase()
        self.default_user, self.default_pass = "user", "pass"

        if self.is_first_time_running() == True:
            self.initiate_database(self.default_user, self.default_pass)
            self.create_marker_file()

        #Initialise GUI components
        self.frame_list = self.initiate_frames()
        self.stack_frames(self.frame_list)
        self.raise_frame("Home_Frame")
        self.populate_navbars(self.frame_list)

    def initiate_frames(self):
        self.home_frame = homeframe.Home_Frame(self, has_navbar=False, navbar_name = "Home")
        self.login_frame = loginframe.Login_Frame(self, has_navbar=False)
        self.signup_frame = signupframe.Signup_Frame(self, has_navbar=False)
        self.options_frame = optionsframe.Options_Frame(self, has_navbar=True, navbar_name = "Options")
        self.filter_frame = filterframe.Filter_Frame(self,has_navbar=True, navbar_name = "Filter")
        self.log_frame = logframe.Log_Frame(self, has_navbar=True, navbar_name="Statistics")
        return[self.login_frame, self.home_frame, self.signup_frame, self.options_frame, self.filter_frame, self.log_frame]
    
    def populate_navbars(self, frame_list):
        for frame in frame_list:
            if frame.has_navbar == True:
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



if __name__ == "__main__" :
    app = Application()
    app.mainloop()