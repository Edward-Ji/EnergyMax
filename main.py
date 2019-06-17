from settings import *

import kivy

from loginview import LoginView
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

# configure window
Config.set("graphics", "resizable", False)
Config.set("kivy", "window_icon", "res/icon.png")

# kivy version requirements
kivy.require("1.10.1")

# load kivy support files
Builder.load_file("loginview.kv")
Builder.load_file("mainview.kv")
Builder.load_file("cartview.kv")

# initiate a single settings instance
Settings.start()


class AppScreenManager(ScreenManager):
    pass


class EnergyMaxApp(App):

    def build(self):
        return LoginView()


EnergyMaxApp().run()
