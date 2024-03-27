from Frames.custom_components import Container, Scrolable_Container, Custom_Frame
import customtkinter as ctk

class Home_Frame(Custom_Frame):
    def __init__(self, App, has_navbar, navbar_name = None):
        super().__init__(App, has_navbar=has_navbar, navbar_name=navbar_name)

    def initialise_containers(self, App):
        self.main_container = Container(self, App, isCentered=True)

    def populate_containers(self, App):
        self.main_label = ctk.CTkLabel(self.main_container, text="Packet FIlter")
        self.main_label.grid(row=0, column=0, columnspan = 2, pady=App.uniform_padding_y)

        self.loginButton = ctk.CTkButton(self.main_container, text="Login", command=lambda:App.raise_frame("Login_Frame"))
        self.loginButton.grid(row=1, column=0, padx=App.uniform_padding_x)

        self.signupButton = ctk.CTkButton(self.main_container, text="Add Account", command=lambda:App.raise_frame("Signup_Frame"))
        self.signupButton.grid(row=1, column=1, padx=App.uniform_padding_x)