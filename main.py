import customtkinter as ctk
from Frames import homeframe, loginframe, signupframe, optionsframe, miframe, protocolfilterframe, portfilterframe, addressfilterframe
import json
import os
from datamanager import Data_Manager

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Set Default Settings
        self.geometry("1000x700")
        self.title("Firewall")
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("green")
        ctk.set_widget_scaling(1.2)
        self.uniform_padding_x = (5,5)
        self.uniform_padding_y = (5,5)
        self.current_theme_name = "green"
        self.theme = self.open_theme(self.current_theme_name)   
        self.navbar_color = self.theme["CTkButton"]["fg_color"][1]
        self.conn, self.cur = Data_Manager.connectToDatabase()
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
        self.mi_frame = miframe.MI_Frame(self, has_navbar=True, navbar_name = "Machine Learning")
        self.protocol_frame = protocolfilterframe.Protocol_Frame(self, has_navbar=True, navbar_name = "Filter Protocols")
        self.port_frame = portfilterframe.Port_Frame(self, has_navbar=True, navbar_name = "Filter Ports")
        self.address_frame = addressfilterframe.Address_Frame(self,has_navbar=True, navbar_name = "Filter Addresses")
        return[self.login_frame, self.home_frame, self.signup_frame, self.options_frame, self.mi_frame, self.port_frame, self.protocol_frame, self.address_frame]
    
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

    def open_theme(self, theme):
        file = open("Data/Themes/"+theme+".json")
        theme = json.load(file)
        file.close()
        return theme
    
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
        Data_Manager.createDatabase(self.conn, self.cur)
        Data_Manager.insertUser(self.conn, self.cur, default_user, default_pass)



if __name__ == "__main__" :
    app = Application()
    app.mainloop()