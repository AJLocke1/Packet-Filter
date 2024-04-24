from UI.Frames import exceptionframe, settingsframe, utilitiesframe, whitelistframe, loginframe, signupframe, helpframe
class UI_Manager():
    def __init__(self, App):
        self.app = App

    def start_ui(self):
        self.app.frame_list = self.initiate_frames()
        self.stack_frames()
        self.populate_navbars()
        if self.app.settings["bypass login"] == "True":
            self.raise_frame("Whitelist_Frame")
        else:
            self.raise_frame("Login_Frame")

    def on_ui_setting_change(self):
        for frame in self.app.frame_list:
            frame.destroy()

        self.app.settings = self.app.data_manager.read_settings()
        self.app.set_settings(self.app.settings)

        self.app.data_manager.update_setting("fullscreen", str(self.app.attributes("-fullscreen")))

        self.app.frame_list = self.initiate_frames()
        self.stack_frames()
        self.populate_navbars()
        self.raise_frame("Settings_Frame")

    def initiate_frames(self):
        App = self.app
        App.login_frame = loginframe.Login_Frame(App, has_navbar=False)
        App.signup_frame = signupframe.Signup_Frame(App, has_navbar=False)
        App.whitelist_frame = whitelistframe.Whitelist_Frame(App,has_navbar=True, navbar_name = "Whitelists")
        App.rule_frame = exceptionframe.Exception_Frame(App, has_navbar=True, navbar_name="Exceptions")
        App.utilities_frame = utilitiesframe.Utilities_Frame(App, has_navbar=True, navbar_name="Utilities")
        App.settings_frame = settingsframe.Settings_Frame(App, has_navbar=True, navbar_name = "Settings")
        App.help_frame = helpframe.Help_Frame(App, has_navbar=True, navbar_name="Help")
        return [App.login_frame, App.signup_frame, App.whitelist_frame, App.rule_frame, App.settings_frame, App.utilities_frame, App.help_frame]
    
    def populate_navbars(self):
        for frame in self.app.frame_list:
            if frame.has_navbar is True:
                frame.navbar.populate_navbar(frame, self.app, self.app.frame_list)

    def stack_frames(self):
        for frame in self.app.frame_list:
            frame.place(relx=0.5, rely=0.5, anchor="center" ,relwidth = 1, relheight = 1)

    def raise_frame(self, frame_string):
        for frame in self.app.frame_list:
            if frame.__class__.__name__ == frame_string:
                frame.tkraise()

    
