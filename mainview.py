from person import *

import pickle
from os.path import isfile

from kivy.properties import BoundedNumericProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

ITEM_DATA = "res/items.p"
DISMISS_MSG = "\n\n[i]Click anywhere else to close"


class ToolBarButton(Button):

    def __init__(self, **kwargs):
        super(ToolBarButton, self).__init__(**kwargs)
        self.drop_down = DropDown(auto_width=False,
                                  width=2*self.width)


class MainButton(Button):
    pass


class DropDownButton(MainButton):
    pass


class ProfileButton(ToolBarButton):

    popup = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(ProfileButton, self).__init__(*args, **kwargs)

        # add functional elements to drop down menu
        profile_btn = DropDownButton(text="Profile")
        # profile_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "profile_screen"))
        profile_btn.bind(on_release=self.drop_down.dismiss)
        self.drop_down.add_widget(profile_btn)

        log_out_btn = DropDownButton(text="Log Out")
        log_out_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "login_screen"))
        log_out_btn.bind(on_release=self.drop_down.dismiss)
        self.drop_down.add_widget(log_out_btn)

        # open drop down when mouse is released on button
        self.bind(on_release=self.drop_down.open)


class CartButton(ToolBarButton):

    def __init__(self, *args, **kwargs):
        super(CartButton, self).__init__(*args, **kwargs)

        # add functional elements to drop down menu
        pay_btn = DropDownButton(text="Pay")
        pay_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "pay_screen"))
        pay_btn.bind(on_release=self.drop_down.dismiss)
        self.drop_down.add_widget(pay_btn)
        self.bind(on_release=self.drop_down.open)


class ToolBar(BoxLayout):
    pass


class ItemView(BoxLayout):

    name = StringProperty()
    img = StringProperty()
    price = NumericProperty()
    quantity = BoundedNumericProperty(0, min=0, max=99)

    def __init__(self, name, img, price):
        self.name = name
        if isfile("res/item_img/" + img):
            self.img = img
        else:
            self.img = "unknown_item.png"
        self.price = price
        super(ItemView, self).__init__()

    def item_action(self, value):
        try:
            self.quantity += value
        except ValueError:
            return


class ItemLayout(GridLayout):

    def __init__(self, **kwargs):
        super(ItemLayout, self).__init__(**kwargs)
        # dynamically add item views according to data file
        with open(ITEM_DATA, 'br') as f:
            item_data = pickle.load(f)
        for item_info in item_data:
            self.add_widget(ItemView(*item_info))
