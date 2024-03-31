from Frames.custom_components import Container, Scrolable_Container, Custom_Frame, Sidebar, Options_Container
import customtkinter as ctk
from os import listdir
from os.path import isfile, join

class Options_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 10)

    def initialise_containers(self, App):
        self.main_container = Scrolable_Container(self, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=1, column=1)

        #the subcontainers of the main container
        self.user_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="User")
        self.user_option_container.grid_columnconfigure(0, weight = 1)
        self.filter_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Filter")
        self.filter_option_container.grid_columnconfigure(0, weight = 1)
        self.UI_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="UI")
        self.UI_option_container.grid_columnconfigure(0, weight = 1)

        #The options for the UI subcontainer
        self.change_theme_option_container = Options_Container(self.UI_option_container, App, row = 0, column = 0, title="Change Theme", description="Change the look of the application.")
        self.change_appearance_option_container = Options_Container(self.UI_option_container, App, row = 1, column = 0, title="Change Appearance Mode", description="Select light or dark mode.")
        self.change_wiget_scaling_container = Options_Container(self.UI_option_container, App, row = 2, column = 0, title="Change UI component scale", description="Increase or decreasee the size of all UI components. Note large values may not work well with small windows")
        self.subcontainers = [self.UI_option_container, self.user_option_container, self.filter_option_container]

        #The options for the user subcontainer
        self.change_user_container = Options_Container(self.user_option_container, App, row = 0, column = 0, title="Change User Credentials", description="Change the user credentials to acccess the application, ensure to make note of the username and password chosen as there is no way to restore the infomation if forgoten")
        self.allow_bypass_login_container = Options_Container(self.user_option_container, App, row =1, column=0, title="Bypass Login on Startup", description="When enabled automatic login will be enabled, allowing for use of the application without loging in")

        #the options for the filter subcontainer
        self.enable_machine_learning_container = Options_Container(self.filter_option_container, App, row=0, column=0, title="Enable Machine Learning", description="Toggle whether a machine learning alogrithm will be used alongside user created rules for filtering")
        self.set_machine_learning_priority = Options_Container(self.filter_option_container, App, row = 1, column = 0, title="Set Machine Learning Priority", description="Set whether the machine learning algorithm will take priority over the user created rules")
        self.disable_filter = Options_Container(self.filter_option_container, App,  row = 2, column=0, title="Disable Filtering", description="Disable all packet filtering functionality")

        #Create the sidebar
        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Options", subcontainers=self.subcontainers, loadedcontainer=self.UI_option_container)

    def populate_containers(self, App):
        self.populate_change_theme_option_container(App, self.change_theme_option_container)
        self.populate_change_appearance_option_container(App, self.change_appearance_option_container)
        self.populate_change_widget_scaling_container(App, self.change_wiget_scaling_container)

    def populate_change_theme_option_container(self, App, container):
        self.theme_dropdown_value = ctk.StringVar(value = App.current_theme_name)
        self.theme_dropdown = ctk.CTkOptionMenu(container, values=[f.split(".", 1)[0] for f in listdir("Data/Themes/") if isfile(join("Data/Themes/", f))], command=lambda value: self.change_theme(App), variable=self.theme_dropdown_value)
        self.theme_dropdown.grid(row=container.row_offset+1, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

    def change_theme(self, App):
        value = self.theme_dropdown_value.get()
        App.data_manager.update_setting("theme", value)
        App.on_setting_change()

    def populate_change_appearance_option_container(self, App, container):
        self.dark_label = ctk.CTkLabel(container, text="Dark Mode")
        self.dark_label.grid(row=container.row_offset+1, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.appearance_mode_radio_value = ctk.StringVar(value = App.appearance_mode_string)
        self.appearance_mode_radio = ctk.CTkSwitch(container, text="Light Mode", command= lambda: self.toggle_appearance_mode(App), variable=self.appearance_mode_radio_value, onvalue="Light", offvalue="Dark")
        self.appearance_mode_radio.grid(row=container.row_offset+1, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

    def toggle_appearance_mode(self, App):
        value = self.appearance_mode_radio_value.get()
        App.data_manager.update_setting("appearance mode", value)
        App.on_setting_change()

    def populate_change_widget_scaling_container(self, App, container):
        self.widget_scale_dropdown_value = ctk.StringVar(value = App.widget_scaling_value)
        self.widget_scale_dropdown = ctk.CTkOptionMenu(container, values=["25","50","65","75","85","100","115","125","150"], command=lambda value: self.change_scale(App), variable=self.widget_scale_dropdown_value)
        self.widget_scale_dropdown.grid(row=container.row_offset+1, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
    
    def change_scale(self, App):
        value = int((self.widget_scale_dropdown_value.get()))/100
        App.data_manager.update_setting("widget scaling", value)
        App.on_setting_change()

