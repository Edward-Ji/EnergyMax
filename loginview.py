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
        msg = Person(self.usr_input.text, self.psw_input.text).login()

        # if there is an error message display a popup
        if not msg:
            msg = "Login success"
        popup_label = Label(text=msg + DISMISS_MSG, markup=True, color=(1, 1, 1, 1))
        popup = Popup(title="Login failed",
                      content=popup_label,
                      size_hint=(.5, None),
                      height=300)

        # save username and password for next run if remember check
        if self.remember_check.state:
            pass

        popup.open()


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
        self.warned = False
        self.state = Settings.retrieve("remember_psw", "normal")

    def on_state(self, instance, value):

        if value == "down" and not self.warned:
            popup = Popup(title="Warning!",
                          content=Label(text="This settings could result in weaker security.",
                                        markup=True,
                                        color=(1, 1, 1, 1)),
                          size_hint=(.5, None),
                          height=180)
            popup.open()
            self.warned = True

        Settings.push("remember_psw", value)

        return super(RememberCheck, self).on_state(instance, value)


class LoginView(BoxLayout):
    pass
