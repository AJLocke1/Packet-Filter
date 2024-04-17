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
        self.grid_columnconfigure(0, weight = 1)

        #the subcontainers of the main container
        self.user_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="User")
        self.user_option_container.grid_columnconfigure(0, weight = 1)
        self.filter_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Filter")
        self.filter_option_container.grid_columnconfigure(0, weight = 1)
        self.log_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="Logs")
        self.log_option_container.grid_columnconfigure(0, weight = 1)
        self.UI_option_container = Container(self.main_container, App, isCentered=False, color=App.frame_color_2, sticky="nsew", padx=App.uniform_padding_x, pady=App.uniform_padding_y, row=0, column=0, name="UI")
        self.UI_option_container.grid_columnconfigure(0, weight = 1)
        
        self.subcontainers = [self.UI_option_container, self.user_option_container, self.filter_option_container, self.log_option_container]

        #The options for the UI subcontainer
        self.change_theme_option_container = Options_Container(self.UI_option_container, App, row = 0, column = 0, title="Change Theme", description="Change the look of the application.")
        self.change_appearance_option_container = Options_Container(self.UI_option_container, App, row = 1, column = 0, title="Change Appearance Mode", description="Select light or dark mode.")
        self.change_wiget_scaling_container = Options_Container(self.UI_option_container, App, row = 2, column = 0, title="Change UI component scale", description="Increase or decreasee the size of all UI components. Note large values may not work well with small windows")

        #The options for the user subcontainer
        self.change_user_container = Options_Container(self.user_option_container, App, row = 0, column = 0, title="Change User Credentials", description="Change the user credentials to acccess the application, ensure to make note of the username and password chosen as there is no way to restore the infomation if forgoten")
        self.allow_bypass_login_container = Options_Container(self.user_option_container, App, row =1, column=0, title="Bypass Login on Startup", description="When enabled automatic login will be enabled, allowing for use of the application without loging in")

        #the options for the filter subcontainer
        self.enable_machine_learning_container = Options_Container(self.filter_option_container, App, row=0, column=0, title="Enable Machine Learning", description="Toggle whether a machine learning alogrithm will be used alongside user created rules for filtering")
        self.set_machine_learning_priority_container = Options_Container(self.filter_option_container, App, row = 1, column = 0, title="Set Machine Learning Priority", description="Set whether the machine learning algorithm will take priority over the user created rules. High means the machine learnings classification will overide the rules classification. Low means both the rules and machine learnings classifiaction will have to accept the packet.")
        self.disable_filter_container = Options_Container(self.filter_option_container, App,  row = 2, column=0, title="Enable Filtering", description="Enable all packet filtering functionality. On by default. Dont't turn off unless necessary")
        self.killswitch_container = Options_Container(self.filter_option_container, App, row =3, column = 0, title="Killswitch", description="Disable all packet flow in and out of the network.")
        self.whitelist_strictness_container = Options_Container(self.filter_option_container, App, row=4, column= 0, title="Whitelist Strictness", description="Decide how strict the whitelists are. if turned on for traffic to be allowed through it must be whitelisted. Defualt behaviour allows for packets with types that have not been specified under any whitelist to still be allowed through. This setting can be changed for each whitelist catagory.")

        #the options for the log subcontainer
        self.enable_logs_container = Options_Container(self.log_option_container, App, row=0, column =0, title="Enable Logs", description="Enable whether the application will keep track of any packets it filters alongside the rules that filtered them")
        self.set_log_auto_delete_container = Options_Container(self.log_option_container, App, row=1, column=0, title="Logs Auto Delete", description="set the time needed before a log file deletes itself")

        #Create the sidebar
        self.sidebar_container = Sidebar(self, App, padx=App.uniform_padding_x, pady=App.uniform_padding_y, title="Options", subcontainers=self.subcontainers, loadedcontainer=self.UI_option_container)

    def populate_containers(self, App):
        self.populate_change_theme_option_container(App, self.change_theme_option_container)
        self.populate_change_appearance_option_container(App, self.change_appearance_option_container)
        self.populate_change_widget_scaling_container(App, self.change_wiget_scaling_container)

        self.populate_change_user_container(App, self.change_user_container)
        self.populate_allow_bypass_login_container(App, self.allow_bypass_login_container)

        self.populate_enable_machine_learning_container(App, self.enable_machine_learning_container)
        self.populate_set_machine_learning_priority_container(App, self.set_machine_learning_priority_container)
        self.populate_disable_filter_container(App, self.disable_filter_container)
        self.populate_killswitch_container(App, self.killswitch_container)
        self.populate_whitelist_strictness_container(App, self.whitelist_strictness_container)

        self.populate_enable_logs_container(App, self.enable_logs_container)
        self.populate_set_log_auto_delete_container(App, self.set_log_auto_delete_container)

    def populate_change_theme_option_container(self, App, container):
        self.theme_dropdown_value = ctk.StringVar(value = App.current_theme_name)
        self.theme_dropdown = ctk.CTkOptionMenu(container, values=[f.split(".", 1)[0] for f in listdir("Data/Themes/") if isfile(join("Data/Themes/", f))], command=lambda value: self.change_theme(App), variable=self.theme_dropdown_value)
        self.theme_dropdown.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky = "w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def change_theme(self, App):
        value = self.theme_dropdown_value.get()
        App.data_manager.update_setting("theme", value)
        App.on_setting_change()

    def populate_change_appearance_option_container(self, App, container):
        self.dark_label = ctk.CTkLabel(container, text="Dark Mode")
        self.dark_label.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.appearance_mode_switch_value = ctk.StringVar(value = App.appearance_mode_string)
        self.appearance_mode_switch = ctk.CTkSwitch(container, text="Light Mode", command= lambda: self.toggle_appearance_mode(App), variable=self.appearance_mode_switch_value, onvalue="Light", offvalue="Dark")
        self.appearance_mode_switch.grid(row=container.row_offset, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_appearance_mode(self, App):
        value = self.appearance_mode_switch_value.get()
        App.data_manager.update_setting("appearance mode", value)
        App.on_setting_change()

    def populate_change_widget_scaling_container(self, App, container):
        self.widget_scale_dropdown_value = ctk.StringVar(value = App.widget_scaling_value)
        self.widget_scale_dropdown = ctk.CTkOptionMenu(container, values=["25","50","65","75","85","100","115","125","150"], command=lambda value: self.change_scale(App), variable=self.widget_scale_dropdown_value)
        self.widget_scale_dropdown.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)
    
    def change_scale(self, App):
        value = int((self.widget_scale_dropdown_value.get()))/100
        App.data_manager.update_setting("widget scaling", value)
        App.on_setting_change()

    def populate_change_user_container(self, App, container):
        self.userEntry = ctk.CTkEntry(container, placeholder_text="Username")
        self.userEntry.grid(pady=12, padx=10, row=container.row_offset, column=0, sticky = "w")

        self.passEntry = ctk.CTkEntry(container, placeholder_text="Password", show="*")
        self.passEntry.grid(pady=12, padx=10, row=container.row_offset+1, column=0, sticky ="w") 

        self.passConfirmationEntry = ctk.CTkEntry(container, placeholder_text="Re enter Password", show="*")
        self.passConfirmationEntry.grid(pady=12, padx=10, row=container.row_offset+2, column=0, sticky = "w") 

        self.change_user_info_label = ctk.CTkLabel(container, text="")
        self.change_user_info_label.grid(pady=6, padx=10, row=container.row_offset+3, column=0, sticky = "w")
        self.change_user_info_label.grid_remove()

        self.loginButton = ctk.CTkButton(container, text="Change", command=lambda : self.change_user_details(App, self.userEntry.get(), self.passEntry.get(), self.passConfirmationEntry.get()))
        self.loginButton.grid(pady=12, padx=10, row=container.row_offset+5, column=0, sticky = "w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def change_user_details(self, App, username, password, passsword_confirmation):
        if password == passsword_confirmation:
            App.data_manager.removeUsers(App.conn, App.cur)
            App.data_manager.insertUser(App.conn, App.cur, username, password)
            self.change_user_info_label.grid()
            self.change_user_info_label.configure(text = "User Details Updated", text_color="green")
            self.userEntry.delete(0, len(username))
            self.passEntry.delete(0, len(password))
            self.passConfirmationEntry.delete(0, len(passsword_confirmation))
            App.after(10000, lambda : (self.change_user_info_label.grid_remove()))
        else:
            self.change_user_info_label.grid()
            self.change_user_info_label.configure(text = "Passwords do not Match", text_color="red")

    def populate_allow_bypass_login_container(self, App, container):
        self.deny_bypass_label = ctk.CTkLabel(container, text="Deny")
        self.deny_bypass_label.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.bypass_login_switch_value = ctk.StringVar(value = App.bypass_login_string)
        self.bypass_login_switch = ctk.CTkSwitch(container, text="Allow", command= lambda: self.toggle_bypass_login(App), variable=self.bypass_login_switch_value, onvalue="True", offvalue="False")
        self.bypass_login_switch.grid(row=container.row_offset, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_bypass_login(self, App):
        value = self.bypass_login_switch_value.get()
        App.data_manager.update_setting("bypass login", value)

    def populate_enable_machine_learning_container(self, App, container):
        self.disable_ML_label = ctk.CTkLabel(container, text="Disable")
        self.disable_ML_label.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.enable_ML_switch_value = ctk.StringVar(value = App.enable_ML_string)
        self.enable_ML_switch = ctk.CTkSwitch(container, text="Enable", command= lambda: self.toggle_ML(App), variable=self.enable_ML_switch_value, onvalue="True", offvalue="False")
        self.enable_ML_switch.grid(row=container.row_offset, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_ML(self, App):
        value = self.enable_ML_switch_value.get()
        App.data_manager.update_setting("enable machine learning", value)

    def populate_set_machine_learning_priority_container(self, App, container):
        self.machine_learning_priority_dropdown_value = ctk.StringVar(value = App.machine_learning_priority)
        self.machine_learning_priority_dropdown = ctk.CTkOptionMenu(container, values=["low", "high"], command=lambda value: self.change_machine_learning_priority(App), variable=self.machine_learning_priority_dropdown_value)
        self.machine_learning_priority_dropdown.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)
        
    def change_machine_learning_priority(self, App):
        value = self.machine_learning_priority_dropdown_value.get()
        App.data_manager.update_setting("machine learning priority", value)


    def populate_disable_filter_container(self, App, container):
        self.disable_filter_label = ctk.CTkLabel(container, text="Disable")
        self.disable_filter_label.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.enable_filter_switch_value = ctk.StringVar(value = App.enable_filter_string)
        self.enable_filter_switch = ctk.CTkSwitch(container, text="Enable", command= lambda: self.toggle_filter(App), variable=self.enable_filter_switch_value, onvalue="True", offvalue="False")
        self.enable_filter_switch.grid(row=container.row_offset, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_filter(self, App):
        value = self.enable_filter_switch_value.get()
        App.data_manager.update_setting("enable filtering", value)

    def populate_killswitch_container(self, App, container):
        self.disable_killswitch_label = ctk.CTkLabel(container, text="Disable")
        self.disable_killswitch_label.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.enable_killswitch_switch_value = ctk.StringVar(value = App.enable_killswitch_string)
        self.enable_killswitch_switch = ctk.CTkSwitch(container, text = "Enable", command= lambda:self.toggle_killswitch(App), variable=self.enable_killswitch_switch_value, onvalue="True", offvalue="False")
        self.enable_killswitch_switch.grid(row=container.row_offset, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_killswitch(self, App):
        value = self.enable_killswitch_switch_value.get()
        App.data_manager.update_setting("enable killswitch", value)

    def populate_whitelist_strictness_container(self, App, container):
        self.IP_title_label = ctk.CTkLabel(container, text = "IP Address:")
        self.IP_title_label.grid(row=container.row_offset, column=0  ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
        
        self.IP_unstrict_strictness_label = ctk.CTkLabel(container, text="Normal")
        self.IP_unstrict_strictness_label.grid(row=container.row_offset, column=1 ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.IP_strictness_switch_value = ctk.StringVar(value = App.IP_whitelist_strictness_string)
        self.IP_strictness_switch = ctk.CTkSwitch(container, text = "Strict", command=lambda:self.toggle_strictness(App, "IP"), variable=self.IP_strictness_switch_value, onvalue="Strict", offvalue="Unstrict")
        self.IP_strictness_switch.grid(row = container.row_offset, column=2,  padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.MAC_title_label = ctk.CTkLabel(container, text = "MAC Address:")
        self.MAC_title_label.grid(row=container.row_offset+1, column=0  ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
        
        self.MAC_unstrict_strictness_label = ctk.CTkLabel(container, text="Normal")
        self.MAC_unstrict_strictness_label.grid(row=container.row_offset+1, column=1 ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.MAC_strictness_switch_value = ctk.StringVar(value = App.MAC_whitelist_strictness_string)
        self.MAC_strictness_switch = ctk.CTkSwitch(container, text = "Strict", command=lambda:self.toggle_strictness(App, "MAC"), variable=self.MAC_strictness_switch_value, onvalue="Strict", offvalue="Unstrict")
        self.MAC_strictness_switch.grid(row = container.row_offset+1, column=2,  padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.port_title_label = ctk.CTkLabel(container, text = "Port:")
        self.port_title_label.grid(row=container.row_offset+2, column=0  ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
        
        self.port_unstrict_strictness_label = ctk.CTkLabel(container, text="Normal")
        self.port_unstrict_strictness_label.grid(row=container.row_offset+2, column=1 ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.port_strictness_switch_value = ctk.StringVar(value = App.port_whitelist_strictness_string)
        self.port_strictness_switch = ctk.CTkSwitch(container, text = "Strict", command=lambda:self.toggle_strictness(App, "port"), variable=self.port_strictness_switch_value, onvalue="Strict", offvalue="Unstrict")
        self.port_strictness_switch.grid(row = container.row_offset+2, column=2,  padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
        
        self.protocol_title_label = ctk.CTkLabel(container, text = "Protocol:")
        self.protocol_title_label.grid(row=container.row_offset+3, column=0  ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
        
        self.protocol_unstrict_strictness_label = ctk.CTkLabel(container, text="Normal")
        self.protocol_unstrict_strictness_label.grid(row=container.row_offset+3, column=1 ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.protocol_strictness_switch_value = ctk.StringVar(value = App.protocol_whitelist_strictness_string)
        self.protocol_strictness_switch = ctk.CTkSwitch(container, text = "Strict", command=lambda:self.toggle_strictness(App, "protocol"), variable=self.protocol_strictness_switch_value, onvalue="Strict", offvalue="Unstrict")
        self.protocol_strictness_switch.grid(row = container.row_offset+3, column=2,  padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.application_title_label = ctk.CTkLabel(container, text = "Application:")
        self.application_title_label.grid(row=container.row_offset+4, column=0  ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")
        
        self.application_unstrict_strictness_label = ctk.CTkLabel(container, text="Normal")
        self.application_unstrict_strictness_label.grid(row=container.row_offset+4, column=1 ,padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.application_strictness_switch_value = ctk.StringVar(value = App.application_whitelist_strictness_string)
        self.application_strictness_switch = ctk.CTkSwitch(container, text = "Strict", command=lambda:self.toggle_strictness(App, "application"), variable=self.application_strictness_switch_value, onvalue="Strict", offvalue="Unstrict")
        self.application_strictness_switch.grid(row = container.row_offset+4, column=2,  padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_strictness(self, App, Type):
        value = getattr(self, Type + "_strictness_switch_value").get()
        App.data_manager.update_setting(Type+" whitelist strictness", value)

    def populate_enable_logs_container(self, App, container):
        self.disable_logs_label = ctk.CTkLabel(container, text="Disable")
        self.disable_logs_label.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.enable_logs_switch_value = ctk.StringVar(value = App.enable_logs_string)
        self.enable_logs_switch = ctk.CTkSwitch(container, text="Enable", command= lambda: self.toggle_logs(App), variable=self.enable_logs_switch_value, onvalue="True", offvalue="False")
        self.enable_logs_switch.grid(row=container.row_offset, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)

    def toggle_logs(self, App):
        value = self.enable_logs_switch_value.get()
        App.data_manager.update_setting("enable logs", value)
    
    def populate_set_log_auto_delete_container(self, App, container):
        self.log_auto_delete_dropdown_value = ctk.StringVar(value = App.log_auto_delete_interval)
        self.log_auto_delete_dropdown = ctk.CTkOptionMenu(container, values=["1 Day", "5 Days", "1 Week", "2 Weeks", "1 Month", "3 Months", "6 Months", "1 Year", "Never"], command=lambda value: self.change_log_auto_delete_time(App), variable=self.log_auto_delete_dropdown_value)
        self.log_auto_delete_dropdown.grid(row=container.row_offset, column=0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        container.instantiate_components(container.master, App, container.title, container.description)
        
    def change_log_auto_delete_time(self, App):
        value = self.log_auto_delete_dropdown_value.get()
        App.data_manager.update_setting("log auto delete interval", value)