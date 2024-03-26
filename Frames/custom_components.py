import customtkinter as ctk

#_____CUSTOM_FRAME_________________________________________________________________________________
class Cutsom_Frame(ctk.CTkFrame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App)
        self.has_navbar = has_navbar
        self.navbar_name = navbar_name
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
        self.grid(row=0, column=0, columnspan=master_columns)
    
    def populate_navbar(self, master, App, frame_list):
        #is a button because labels are slightly bigger
        self.label = ctk.CTkButton(self,text="Packet Filter", height=30, corner_radius=0,hover_color=App.navbar_color)
        self.label.grid(column=0, row=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        self.buttons = []
        count = 0
        for i in range(len(frame_list)):
            if frame_list[i].has_navbar == True or frame_list[i].navbar_name != None:
                frame = frame_list[i].__class__.__name__
                #f frame needs to be used due to a binding issue taking the value of teh wrong iteration of frame.
                self.buttons.append(ctk.CTkButton(self, text=frame_list[i].navbar_name, height=30, corner_radius=0, command=lambda f=frame: App.raise_frame(f)))
                self.buttons[count].grid(column=count+1, row=0, sticky="nsew")
                self.grid_columnconfigure(count+1, weight=1)
                count +=1
            
            

