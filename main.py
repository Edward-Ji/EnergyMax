from settings import *

import kivy

from loginview import *
from mainview import *
from payview import *
from wheelview import *
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# configure window size, color and icon
Window.clearcolor = (0.8, 0.8, 1, 1)
Config.set("graphics", "resizable", False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# kivy version requirements
kivy.require("1.10.1")

# load kivy support files
Builder.load_file("loginview.kv")
Builder.load_file("mainview.kv")
Builder.load_file("cartview.kv")
Builder.load_file("payview.kv")
Builder.load_file("wheelview.kv")

# initiate a single settings instance
Settings.start()


class AppScreenManager(ScreenManager):
    pass


class EnergyMaxApp(App):

    def build(self):
        self.icon = "res/icon.ico"
        return AppScreenManager()


EnergyMaxApp().run()
