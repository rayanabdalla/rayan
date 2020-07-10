from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import json, glob
from datetime import datetime
from pathlib import Path
import random
from hoverable import HoverBehavior


Builder.load_file("des.kv")

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "Signup_screen"

    def login(self,uname,pword):
        with open('users.json') as file:
            users = json.load(file) 
        if uname in users and users[uname]["password"] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = " X Incorrect Username or Password! X"


class ImageButton(ButtonBehavior,HoverBehavior,Image,):
    pass



class RootWidget(ScreenManager):
    pass
    
class SignupScreen(Screen):
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users= json.load(file)
        
        users[uname] = {'username':uname,'password':pword,
        'created':datetime.now().strftime("%Y-%M-%D %H-%M-%S")}   
        

        with open ("users.json", "w") as file:
            json.dump(users,file)
           
        self.manager.current ="sign_up_screen_success"

class SignupScreenSuccess(Screen):
    def go_to_login(self):
        
        self.manager.transition.direction = 'right'
        self.manager.current ="LoginScreen"

class LoginScreenSuccess(Screen):
    def Log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "LoginScreen"

    def get_saying(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob('quotes/*txt')

        available_feelings =[Path(filename).stem for filename in   available_feelings]

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
            print(quotes)
        else:
            self.ids.quote.text = "sorry, No Quotes here! :( \n --- try another feeling ---"


class MainApp(App):
    def build(self):
        return RootWidget()  
        
if __name__ =="__main__":
    MainApp().run()   