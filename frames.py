import customtkinter as ctk

#_____CUSTOM_FRAME_________________________________________________________________________________
class Cutsom_Frame(ctk.CTkFrame):
    def __init__(self, App, has_navbar):
        super().__init__(App)
        self.has_navbar = has_navbar
        self.initialise_containers(App)
        self.populate_containers(App)
        if has_navbar == True:
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
    
#_____ALL_FRAMES___________________________________________________________________________________
class Login_Frame(Cutsom_Frame):
    def __init__(self, App, has_navbar):
        super().__init__(App, has_navbar=has_navbar)
    def initialise_containers(self, App):
        self.container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.login_button = ctk.CTkButton(self.container, text="Login", command=lambda: App.raise_frame("Home_Frame"))
        self.login_button.grid(column=0, row=0)

class Home_Frame(Cutsom_Frame):
    def __init__(self, App, has_navbar):
        super().__init__(App, has_navbar=has_navbar)
    def initialise_containers(self, App):
        self.sidebar_container = Container(self, App, isCentered=False, row=1, column=0, color="blue")
        self.main_container = Scrolable_Container(self, App, isCentered=False, row=1, column=1, color="red")

    def populate_containers(self, App):
        self.side_label = ctk.CTkLabel(self.sidebar_container, text="Home")
        self.side_label.grid(row=0, column=0)

        self.main_label = ctk.CTkLabel(self.main_container, text="Main")
        self.main_label.grid(row=0, column=0)

class Signup_Frame(Cutsom_Frame):
    def __init__(self, App, has_navbar):
        super().__init__(App, has_navbar=has_navbar)
    def initialise_containers(self, App):
        self.container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.login_button = ctk.CTkButton(self.container, text="SignUp", command=lambda: App.raise_frame("Home_Frame"))
        self.login_button.grid(column=0, row=0)
        
class Options_Frame(Cutsom_Frame):
    def __init__(self, App, has_navbar):
        super().__init__(App, has_navbar=has_navbar)
    def initialise_containers(self, App):
        self.container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.label = ctk.CTkLabel(self.container, text="Options")
        self.label.grid(row=0, column=0)
        


#_____CONTAINERS____________________________________________________________________________
class Custom_Container():
    def __init__(self, master, App, isCentered, row=None, column=None, color="transparent"):
        super().__init__(master, fg_color=color)
        self.column = column
        self.row = row
        self.configure_placement(isCentered)

    def configure_placement(self, isCentered):
        if isCentered:
            self.place(relx=0.5, rely=0.5, anchor="center")
        else:
            self.grid(column=self.column, row=self.row)

class Container(Custom_Container, ctk.CTkFrame):
    pass

class Scrolable_Container(Custom_Container, ctk.CTkScrollableFrame):
    pass

#_____REUSED_COMPONENTS____________________________________________________________________________
class Navbar(ctk.CTkFrame):
    def __init__(self, master, App):
        super().__init__(master, fg_color=App.navbar_color, border_width=1)
        self.place_navbar(master)
    
    def place_navbar(self, master):
        master_columns = master.grid_size()[0]
        self.grid(row=0, column=0, sticky="nsew", columnspan=master_columns)
    
    def populate_navbar(self, master, App, frame_list):
        self.label = ctk.CTkLabel(self,text="Packet Filter", height=20)
        self.label.grid(column=0, row=0)

        self.buttons = []
        for i in range(len(frame_list)):
            frame = frame_list[i].__class__.__name__
            #f frame needs to be used due to a binding issue taking the value of teh wrong iteration of frame.
            self.buttons.append(ctk.CTkButton(self, text=frame, border_color="black", border_width=1, height=30, corner_radius=0, command=lambda f=frame: App.raise_frame(f)))
            self.buttons[i].grid(column=i+1, row=0)
            

