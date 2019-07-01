import kivy

from loginview import *
from mainview import *
from cartview import *
from wheelview import *
from profileview import *
from receiptview import *
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

# configure window size, color and icon
Window.clearcolor = (0.8, 0.8, 1, 1)
Config.set("input", "mouse", "mouse,multitouch_on_demand")
Config.set('widgets', 'scroll_friction', 0)

# kivy version requirements
kivy.require("1.10.1")

# load kivy support files
Builder.load_file("loginview.kv")
Builder.load_file("mainview.kv")
Builder.load_file("cartview.kv")
Builder.load_file("wheelview.kv")
Builder.load_file("profileview.kv")
Builder.load_file("receiptview.kv")

# initiate a single settings instance
Settings.start()


class AppScreenManager(ScreenManager):

    last_screen = StringProperty()

    def on_current(self, instance, value):
        super(AppScreenManager, self).on_current(instance, value)
        if value == "main_screen":
            self.main_screen.item_layout.refresh()
        elif value == "cart_screen":
            self.cart_screen.cart_layout.refresh()
        elif value == "wheel_screen":
            self.wheel_screen.wheel_layout.check()
        elif value == "profile_screen":
            self.profile_screen.card_layout.refresh()
        elif value == "receipt_screen":
            self.receipt_screen.cart_layout.refresh()
            self.receipt_screen.receipt.refresh()

    def record(self):
        self.last_screen = self.current

    def back(self):
        self.current = self.last_screen


class EnergyMaxApp(App):

    def build(self):
        self.icon = "res/images/icon.ico"
        return AppScreenManager()


EnergyMaxApp().run()
