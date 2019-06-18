from person import *
from settings import *

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton


DISMISS_MSG = "\n\n[i]Click anywhere else to close"
ENCRYPT_CODE = b"Nutrition"


class PasswordEye(ToggleButton):

    def on_press(self):
        if self.text == "Show":
            self.text = "Hide"
            self.psw_input.password = False
        else:
            self.text = "Show"
            self.psw_input.password = True


class LoginButton(Button):

    def on_release(self):
        usr, psw = self.usr_input.text, self.psw_input.text
        msg = Person(usr, psw).login()

        # if there is an error message display a popup
        if msg:
            popup_label = Label(text=msg + DISMISS_MSG, markup=True, color=(1, 1, 1, 1))
            popup = Popup(title="Login failed",
                          content=popup_label,
                          size_hint=(.5, None),
                          height=300)
            popup.open()
        else:

            # save (or not to save) username and password for next run
            if self.remember_check.state == "normal":
                usr, psw = '', ''
                self.usr_input.text = ''
                self.psw_input.text = ''
            Settings.push("login_username", usr)
            Settings.push("login_password", psw)

            self.root.screen_manager.current = "main_screen"


class RegisterButton(Button):

    def on_release(self):
        msg = Person(self.usr_input.text, self.psw_input.text).register()
        # if there is an error message display a popup
        if not msg:
            msg = "Register success"
        popup_label = Label(text=msg + DISMISS_MSG, markup=True, color=(1, 1, 1, 1))
        popup = Popup(title="Register failed",
                      content=popup_label,
                      size_hint=(.5, None),
                      height=300)
        popup.open()


class RememberCheck(CheckBox):

    def __init__(self, **kwargs):
        super(RememberCheck, self).__init__(**kwargs)
        self.warned = True  # prevent popup from opening upon initiation of instance
        self.popup = None
        self.state = Settings.retrieve("remember_psw", "normal")
        self.warned = False

    def on_state(self, instance, value):
        # warn if check for first time
        if value == "down" and not self.warned:
            self.popup = Popup(title="Warning!",
                               content=Label(text="This settings could result in weaker security.",
                                             markup=True,
                                             color=(1, 1, 1, 1)),
                               size_hint=(.5, None),
                               height=180)
            self.popup.open()
            self.warned = True

        Settings.push("remember_psw", value)

        return super(RememberCheck, self).on_state(instance, value)


class LoginView(BoxLayout):
    pass
