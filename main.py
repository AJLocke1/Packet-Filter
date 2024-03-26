import customtkinter as ctk
import frames
import json

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        #Set Default Settings
        self.geometry("600x500")
        self.title("Firewall")
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("green")
        ctk.set_widget_scaling(1.2)
        self.current_theme = "green"
        self.navbar_color = "#2FA572"

        #Initialise GUI components
        self.frame_list = self.initiate_frames()
        self.stack_frames(self.frame_list)
        self.raise_frame("Login_Frame")
        self.populate_navbars(self.frame_list)

    def initiate_frames(self):
        self.login_frame = frames.Login_Frame(self, has_navbar=False)
        self.home_frame = frames.Home_Frame(self, has_navbar=True)
        self.signup_frame = frames.Signup_Frame(self, has_navbar=False)
        self.options_frame = frames.Options_Frame(self, has_navbar=True)
        return[self.login_frame, self.home_frame, self.signup_frame, self.options_frame]
    
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


if __name__ == "__main__" :
    app = Application()
    app.mainloop()