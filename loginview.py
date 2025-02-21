from person import *
from settings import *

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.screenmanager import FadeTransition, CardTransition
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton


dismiss_msg = "[u]or click anywhere else to close"


# show popup with potential button bind
def show_popup(title, message, btn_text=None, btn_bind=None):

    popup_layout = BoxLayout(orientation="vertical")
    popup_layout.add_widget(Label(text=message,
                                  markup=True,
                                  color=(1, 1, 1, 1)))

    # add button if there is an extra functional button
    if btn_text and btn_bind:
        extra_btn = Button(text=btn_text,
                           size_hint=(None, None),
                           size=(85, 50),
                           pos_hint={"center_x": .5})
        for event in btn_bind:
            extra_btn.bind(on_press=event)
        popup_layout.add_widget(extra_btn)

    # add close button last
    close_btn = Button(text="Close",
                       size_hint=(None, None),
                       size=(85, 50),
                       pos_hint={"center_x": .5})
    popup_layout.add_widget(close_btn)

    # create popup object
    popup = Popup(title=title,
                  content=popup_layout,
                  size_hint=(.5, None),
                  height=300)

    # bind all button with dismissing popup event
    if btn_text and btn_bind:
        extra_btn.bind(on_press=popup.dismiss)
    close_btn.bind(on_press=popup.dismiss)

    popup.open()


class InputBox:
    pass


class PasswordEye(ToggleButton):

    def on_press(self):
        if self.text == "Show":
            self.text = "Hide"
            self.psw_input.password = False
            # hide password after shown for 3 seconds
            Clock.schedule_once(lambda t: self.hide(), 3)
        else:
            self.text = "Show"
            self.psw_input.password = True
        return True

    # automatically hide password for better security
    def hide(self):
        self.text = "Show"
        self.psw_input.password = True


class LoginButton(Button):

    def on_release(self):
        usr, psw = self.usr_input.text, self.psw_input.text
        msg = Person(usr, psw).login()

        # if there is an error message display a popup
        if msg:
            show_popup("Login failed", msg)
        else:

            # save (or not to save) username and password for next run
            if self.remember_check.state == "normal":
                usr, psw = '', ''
                self.usr_input.text = ''
                self.psw_input.text = ''
            Settings.push("login_username", usr)
            Settings.push("login_password", psw)

            self.root.screen_manager.transition = CardTransition(direction="up", mode="pop")
            self.root.screen_manager.current = "main_screen"
            self.root.screen_manager.transition = FadeTransition(clearcolor=(.8, .8, 1, 1))


class RegisterButton(Button):

    def on_release(self):
        msg = Person(self.usr_input.text, self.psw_input.text).register()
        # if there is an error message display a popup
        if not msg:
            msg = "You have registered your account.\n Login to start shopping!"
            show_popup("Congratulations", msg)
        else:
            show_popup("Register failed", msg)


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
            show_popup("Warning", "This function could result in weaker security!")
            self.warned = True

        Settings.push("remember_psw", value)


class LoginView(BoxLayout):
    pass
