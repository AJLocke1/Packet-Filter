from Frames.custom_components import Container, Scrolable_Container, Custom_Frame
import customtkinter as ctk

class Signup_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)
    def initialise_containers(self, App):
        self.container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.label = ctk.CTkLabel(self.container, text="Create New User")
        self.label.grid(pady=12, padx=10, row=0, column=0)

        self.userEntry = ctk.CTkEntry(self.container, placeholder_text="Username")
        self.userEntry.grid(pady=12, padx=10, row=1, column=0)

        self.passEntry = ctk.CTkEntry(self.container, placeholder_text="Password", show="*")
        self.passEntry.grid(pady=12, padx=10, row=2, column=0) 

        self.confirmPassEntry = ctk.CTkEntry(self.container, placeholder_text="Password", show="*")
        self.confirmPassEntry.grid(pady=12, padx=10, row=3, column=0) 

        self.errorLabel = ctk.CTkLabel(self.container, text="", text_color="red")
        self.errorLabel.grid(pady=6, padx=10, row=4, column=0)
        self.errorLabel.grid_remove()

        self.loginButton = ctk.CTkButton(self.container, text="Add User", command=lambda : self.signup(App, self.userEntry.get(), self.passEntry.get(), self.confirmPassEntry.get()))
        self.loginButton.grid(pady=12, padx=10, row=5, column=0)

        self.checkBox = ctk.CTkCheckBox(self.container, text="Remember Me")
        self.checkBox.grid(pady=12, padx=10, row=6, column=0)

    def signup(self, App, username, password, password_confirmation):
        App.raise_frame("Address_Frame")