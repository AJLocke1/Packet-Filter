from Frames.custom_components import Container, Scrolable_Container, Cutsom_Frame
import customtkinter as ctk
from datamanager import Data_Manager
import hashlib as hl

class Login_Frame(Cutsom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
    def initialise_containers(self, App):
        self.container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.label = ctk.CTkLabel(self.container, text="Login System")
        self.label.grid(pady=12, padx=10, row=0, column=0)

        self.userEntry = ctk.CTkEntry(self.container, placeholder_text="Username")
        self.userEntry.grid(pady=12, padx=10, row=1, column=0)

        self.passEntry = ctk.CTkEntry(self.container, placeholder_text="Password", show="*")
        self.passEntry.grid(pady=12, padx=10, row=2, column=0) 

        self.errorLabel = ctk.CTkLabel(self.container, text="", text_color="red")
        self.errorLabel.grid(pady=6, padx=10, row=3, column=0)
        self.errorLabel.grid_remove()

        self.loginButton = ctk.CTkButton(self.container, text="Login", command=lambda : self.login(App, self.userEntry.get(), self.passEntry.get()))
        self.loginButton.grid(pady=12, padx=10, row=4, column=0)

        self.checkBox = ctk.CTkCheckBox(self.container, text="Remember Me")
        self.checkBox.grid(pady=12, padx=10, row=5, column=0)

    def login(self, App, username, password):
        try:
            fetched = Data_Manager.findPassword(App.conn, App.cur, username)
            encodedpass = fetched[0][0]
            if hl.sha256(password.encode()).hexdigest() == encodedpass:
                #change frame
                self.App.raise_frame("Address_Filter")
                self.errorLabel.configure(text="")
                self.errorLabel.grid_remove()
            else:
                self.errorLabel.grid()
                self.errorLabel.configure(text= "inccorect password")
        except IndexError:
            encodedpass = ""
            self.errorLabel.grid()
            self.errorLabel.configure(text="User not Found")

