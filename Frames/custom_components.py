import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
import re

#_____CUSTOM_FRAME_________________________________________________________________________________
class Custom_Frame(ctk.CTkFrame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App)
        self.has_navbar = has_navbar
        self.navbar_name = navbar_name
        self.initialise_containers(App)
        self.populate_containers(App)
        if has_navbar is True:
            self.initialise_navbar(App)

    def initialise_containers(self):
        #Each custom frame must define its own containers
        raise NotImplementedError("Subclasses must implement initialise_containers method.")

    def populate_containers(self):
        #Each cusotom frame must populate its own containers
        raise NotImplementedError("Subclasses must implement populate_containers method.")
    
    def initialise_navbar(self, App):
        self.columnconfigure(0, weight=1)
        self.navbar = Navbar(self, App)
        self.rowconfigure(1, weight=1)
    
#_____CONTAINERS____________________________________________________________________________
class Custom_Container():
    def __init__(self, master, App, isCentered, row=None, column=None, color="transparent", sticky=None, padx=None, pady=None, max_width = None, name=None, placeself = None):
        super().__init__(master, fg_color=color)
        self.filter_container_head = None
        self.name = name
        self.column = column
        self.row = row
        self.max_width = max_width
        self.configure_placement(isCentered, sticky, padx, pady, max_width, placeself)

    def configure_placement(self, isCentered, sticky, padx, pady, max_width, placeself):
        if placeself is None:
            if isCentered:
                self.place(relx=0.5, rely=0.5, anchor="center", padx = padx, pady = pady)
            else:
                self.grid(column=self.column, row=self.row, sticky=sticky, padx = padx, pady = pady)

            if self.max_width:
                self.configure(width=self.max_width)
        else:
            pass

    def raise_subcontainer(self, Subcontainer):
        Subcontainer.lift()

class Container(Custom_Container, ctk.CTkFrame):
    pass

class Scrolable_Container(Custom_Container, ctk.CTkScrollableFrame):
    pass

#_____REUSED_COMPONENTS____________________________________________________________________________
class Navbar(ctk.CTkFrame):
    def __init__(self, master, App):
        super().__init__(master, fg_color=App.theme_color, border_width=1)
        self.image = ctk.CTkImage(light_image=Image.open("Data/Images/firewallicon.png"),dark_image=Image.open("Data/Images/firewalliconLight.png"))
        self.place_navbar(master)
    
    def place_navbar(self, master):
        master_columns = master.grid_size()[0]
        self.grid(row=0, column=0, columnspan=master_columns, sticky = "ew")
    
    def populate_navbar(self, master, App, frame_list):
        #is a button because labels are slightly bigger
        self.label = ctk.CTkButton(self,text="Packet Filter", height=30, corner_radius=0,hover_color=App.theme_color)
        self.label.grid(column=0, row=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        self.filterImage = ctk.CTkButton(self,image=self.image, height=30, corner_radius=0,hover_color=App.theme_color, text="", width =30)
        self.filterImage.grid(column=1, row=0, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)

        self.buttons = []
        count = 0
        for i in range(len(frame_list)):
            if frame_list[i].has_navbar is True or frame_list[i].navbar_name is not None:
                frame = frame_list[i].__class__.__name__
                #f frame needs to be used due to a binding issue taking the value of teh wrong iteration of frame.
                self.buttons.append(ctk.CTkButton(self, text=frame_list[i].navbar_name, height=30, corner_radius=0, command=lambda f=frame: App.raise_frame(f)))
                self.buttons[count].grid(column=count+2, row=0, sticky="nsew")
                self.grid_columnconfigure(count+2, weight=1)
                count +=1

class Sidebar_Button(ctk.CTkButton):
    def __init__(self, master, App, text_color, **kwargs):
        super().__init__(master, fg_color="transparent", width=60, text_color = text_color, **kwargs)
        self.bind("<Button-1>", lambda event: self.change_color(App))

    def change_color(self, App):
        if self.master.lastclicked is not None:
            self.master.lastclicked.configure(fg_color = "transparent") 
        self.configure(fg_color=App.theme_color)
        self.master.lastclicked = self

class Sidebar(Container):
    def __init__(self, master, App, title,  subcontainers, loadedcontainer, padx = None, pady = None):
        self.color = App.frame_color
        super().__init__(master, App, isCentered=False, color=self.color, row = 1, column =0, sticky="ns")
        self.lastclicked = None
        self.title = title
        self.subcontainers = subcontainers
        self.loaded_container = loadedcontainer

        self.populate_sidebar_container(App, self.subcontainers, self.title, self.loaded_container)

    def populate_sidebar_container(self, App, subcontainers, title, loaded_container):
        self.title = ctk.CTkLabel(self, text=title, font=("", 30))
        self.title.grid(row=0, column =0, pady=(App.uniform_padding_y[0]*5,App.uniform_padding_y[1]*3))

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(120,10))
        self.seperator = ctk.CTkLabel(self, text="", image=self.seperator_image)
        self.seperator.grid(row=1, column=0)

        if App.appearance_mode_string == "Light":
            self.text_color = "Black"
        else:
            self.text_color = "white"
        for i, subcontainer in enumerate(subcontainers):
            self.button = Sidebar_Button(self, App, text=subcontainer.name, text_color=self.text_color, command=lambda c=subcontainer: self.raise_subcontainer(c))
            self.button.grid(row=i+2, column=0, sticky="ew", pady =App.uniform_padding_y)
            if subcontainer == loaded_container:
                self.button.change_color(App)

class Whitelist_Head(Container):
    def __init__(self, master, App, name, description, padx = None, pady = None):
        self.color = App.frame_color
        super().__init__(master, App, isCentered=False, color=self.color)
        self.image = ctk.CTkImage(light_image=Image.open("Data/Images/PlusSymbol.png"),dark_image=Image.open("Data/Images/PlusSymbolLight.png"))

        self.name = name
        self.description = description
        self.grid(row=0, column=0, sticky="new", padx = padx, pady = pady)
        master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.whitelist_creation_window = None

        self.label = ctk.CTkLabel(self, text=name)
        self.label.grid(row=0, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, sticky="w")

        self.add_whitelist_button = ctk.CTkButton(self, text="", width=30, image=self.image, command = lambda: self.add_whitelist(App, name))
        self.add_whitelist_button.grid(row=0, column = 1, sticky="e", padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label2 = ctk.CTkLabel(self, text=description)
        self.label2.grid(row=1, column = 0, sticky="we", columnspan = 2, padx=[5,5], pady = [5,5])
        self.label2.bind('<Configure>', lambda event: self.update_wraplength())

    def add_whitelist(self, App, name):
        if self.whitelist_creation_window is None or not self.whitelist_creation_window.winfo_exists():
            self.whitelist_creation_window = Whitelist_Creation_Window(self, App, name)  # create window if its None or destroyed
        else:
            self.whitelist_creation_window.focus() 

    def update_wraplength(self):
        self.label2.update_idletasks()
        self.label2.configure(wraplength=self.winfo_width() - 100)

class Whitelist_Creation_Window(ctk.CTkToplevel):
    def __init__(self, master, App, type):
        super().__init__(master)
        self.type = type
        self.is_whitlisted_string = None
        self.direction_string = None

        self.label = ctk.CTkLabel(self, text="Create Rule")
        self.label.grid(row = 0, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y, columnspan = 3, sticky="ew")

        self.Entry = ctk.CTkEntry(self, placeholder_text=type)
        self.Entry.grid(row = 1, column = 0, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_2 = ctk.CTkLabel(self, text="Blacklist")
        self.label_2.grid(row = 1, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.is_whitlisted_value =ctk.StringVar(self.is_whitlisted_string)
        self.is_whitlisted = ctk.CTkSwitch(self, text="Whitelist", variable=self.is_whitlisted_value, onvalue="Whitelist", offvalue="Blacklist")
        self.is_whitlisted.grid(row =1, column = 2, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.label_3 = ctk.CTkLabel(self, text="Outgoing")
        self.label_3.grid(row = 2, column = 1, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.direction_value =ctk.StringVar(self.direction_string)
        self.direction = ctk.CTkSwitch(self, text="Incoming", variable=self.direction_value, onvalue="Incoming", offvalue="Outgoing")
        self.direction.grid(row =2, column = 2, padx=App.uniform_padding_x, pady=App.uniform_padding_y)

        self.enter_whitelist = ctk.CTkButton(self, text = "Enter Whitelist", command=lambda: self.add_whitelist(master, App, self.type, self.Entry.get(), self.is_whitlisted.get(), self.direction.get()))
        self.enter_whitelist.grid(row=2, column=3, padx=App.uniform_padding_x, pady=App.uniform_padding_y, columnspan =3, sticky="ew")

    def add_whitelist(self, master, App, type, target, iswhitelisted, direction):
        is_valid = self.check_whitelist(type, target)
        if is_valid is True:
            if (CTkMessagebox(title="Add Whitelist?", message= "Are you sure you want to "+iswhitelisted+" The "+type+" "+target+" "+direction, option_1="No", option_2="yes")).get() == "yes":
                Added = App.data_manager.add_whitelist(type, target, iswhitelisted, direction, App.cur, App.conn)
                if Added == "Added":
                    Whitelist(master.master.whitelist_table, App, type, target, iswhitelisted, direction)
                self.destroy()
        
    def check_whitelist(self, type, target):
        match type:
            case "Address":
                IPv4_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
                IPv6_regex = "((([0-9a-fA-F]){1,4})\:){7}([0-9a-fA-F]){1,4}"
                IPv4_regex = re.compile(IPv4_regex)
                IPv6_regex = re.compile(IPv6_regex)
                if (re.search(IPv4_regex, target)):
                    return True
                elif (re.search(IPv6_regex, target)):
                    return True
                else:
                    return False
            case "Port":
                try:
                    target = int(target)
                    return True
                except ValueError:
                    return False
            case "Protocol":
                supported_protocols = ["TCP", "UDP", "ICMP", "SCTP", "DCCP", "GRE", "RSVP", "L2TP", "IGMP", "MPLS", "QUIC", "RTP", "SRTP", "LISP", "WireGuard"]
                protocol_numbers = {"TCP": 6, "UDP": 17, "ICMP": 1, "SCTP": 132, "DCCP": 33, "GRE": 47, "RSVP": 46, "L2TP": 115, "IGMP": 2, "MPLS": 137, "QUIC": 17, "RTP": 103, "SRTP": 254, "LISP": 35, "WireGuard": 20}

                if target in supported_protocols or target in protocol_numbers.values:
                    return True
                else:
                    return False
            case "Application":
                try:
                    target = str(target)
                    return True
                except ValueError:
                    return False
                
class Whitelist(Container):
    def __init__(self, master, App, type, target, iswhitelisted, direction, padx = None, pady = None):
        super().__init__(master, App, isCentered=False, color=App.frame_color, placeself = False)

        self.grid_columnconfigure(0, weight=1, uniform="uniform")
        self.grid_columnconfigure(1, weight=1, uniform="uniform")
        self.grid_columnconfigure(2, weight=1, uniform="uniform")
        self.grid_columnconfigure(3, weight=1, uniform="uniform")

        self.instantiate_components(App, type, target, iswhitelisted, direction, padx, pady)
        self.pack(fill = "x", pady = App.uniform_padding_y)
    
    def instantiate_components(self, App, type, target, iswhitelisted, direction, padx, pady):
        self.title = ctk.CTkLabel(self, text=target)
        self.title.grid(row=0, column = 0, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.whitelisted = ctk.CTkLabel(self, text=iswhitelisted)
        self.whitelisted.grid(row=0, column = 1, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.direction = ctk.CTkLabel(self, text=direction)
        self.direction.grid(row=0, column = 2, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

        self.delete_whitelist_button = ctk.CTkButton(self, text="Remove Rule", command=lambda: self.remove_whitelist(App, type, target, iswhitelisted, direction))
        self.delete_whitelist_button.grid(row = 0, column = 3, padx = App.uniform_padding_x, pady=App.uniform_padding_y)

    def remove_whitelist(self, App, type, target, iswhitelisted, direction):
        App.data_manager.remove_whitelist(type, target, iswhitelisted, direction, App.cur, App.conn)
        self.destroy()


class Whitelist_Table(Container):
    def __init__(self, master, App, padx = None, pady = None):
        super().__init__(master, App, isCentered=False, color=App.frame_color_2)

        self.grid(row=2, column=0, sticky="nsew", padx = padx, pady = pady)
        master.grid_columnconfigure(0, weight=1)

        self.load_whitelists(App, master.name)
    
    def load_whitelists(self, App, type):
        whitelists = App.data_manager.fetch_whitelists(App.cur, type)
        for whitelist in whitelists:
            whitelist = Whitelist(self, App, whitelist[1], whitelist[0], whitelist[2], whitelist[3])
            
        

class Whitelist_Container(Scrolable_Container):
    def __init__(self, master, App, name, description, padx = None, pady = None):
        self.color = App.frame_color_2
        super().__init__(master, App, isCentered=False, column = 0, row = 0, sticky="nsew", color=self.color, name = name) 

        self.instantiate_components(App, name, description, padx, pady)
    
    def instantiate_components(self, App, name, description, padx, pady):
        self.whitelist_head = Whitelist_Head(self, App, name, description, padx, pady)
        self.whitelist_table = Whitelist_Table(self, App, padx, pady)

class Options_Container(Container):
    def __init__(self, master, App, title, description, column, row):
        super().__init__(master, App, isCentered=False, column = column, row = row, sticky="nsew", color=App.frame_color_2, padx=App.uniform_padding_x, pady=(App.uniform_padding_y[0], App.uniform_padding_y[1]*6)) 
        self.title = title
        self.description = description
        self.row_offset = 3
        master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight = 1)
    
    def instantiate_components(self, master, App, title, description):
        self.title = ctk.CTkLabel(self, text=title, font=("", 20))
        self.title.grid(row=0, column = 0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(250,10))
        self.seperator = ctk.CTkLabel(self, text="", image=self.seperator_image)
        self.seperator.grid(row=1, column=0, columnspan = self.grid_size()[0], sticky ="w")

        self.description = ctk.CTkLabel(self, text=description, anchor = "w", justify = "left")
        self.description.grid(row=2, column = 0, sticky="we", columnspan = self.grid_size()[0], padx=[5,5], pady = [5,5])
        self.description.bind('<Configure>', lambda event: self.update_wraplength(master))

    def update_wraplength(self, master):
        self.description.update_idletasks()
        self.description.configure(wraplength=master.master.winfo_width() - 100)

class Info_Pannel(Container):
    def __init__(self, master, App, title, body, column, row):
        super().__init__(master, App, isCentered = False, row = row, column = column, color = App.frame_color_2, sticky = "nsew", padx=App.uniform_padding_x, pady=(App.uniform_padding_y[0], App.uniform_padding_y[1]*6))
        self.title = title
        self.body = body
        master.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight = 1)
        self.instantiate_components(master, App, title, body)

    def instantiate_componenets(self, master, App, title, body):
        self.title = ctk.CTkLabel(self, text=title, font=("", 20))
        self.title.grid(row=0, column = 0, pady=(App.uniform_padding_y[0]*2,App.uniform_padding_y[1]*2), sticky="w", columnspan=self.grid_size()[0])

        self.seperator_image = ctk.CTkImage(light_image=Image.open("Data/Images/seperator.png"),dark_image=Image.open("Data/Images/seperatorLight.png"), size=(250,10))
        self.seperator = ctk.CTkLabel(self, text="", image=self.seperator_image)
        self.seperator.grid(row=1, column=0, columnspan = self.grid_size()[0], sticky ="w")

        self.body = ctk.CTkLabel(self, text=body, anchor = "w", justify = "left")
        self.body.grid(row=2, column = 0, sticky="we", columnspan = self.grid_size()[0], padx=[5,5], pady = [5,5])
        self.body.bind('<Configure>', lambda event: self.update_wraplength(master))

    def update_wraplength(self, master):
        self.body.update_idletasks()
        self.body.configure(wraplength=master.master.winfo_width() - 100)
        





    

            
            

