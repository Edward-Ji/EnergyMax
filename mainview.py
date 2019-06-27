from cart import *

from os.path import isfile

from kivy.properties import BoundedNumericProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import FadeTransition, CardTransition
from kivy.uix.scrollview import ScrollView

ITEM_DATA = "res/items.p"
DISMISS_MSG = "\n\n[i]Click anywhere else to close"


class ToolBar(BoxLayout):
    pass


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

    def __init__(self, **kwargs):
        super(ProfileButton, self).__init__(**kwargs)

        # add functional elements to drop down menu
        profile_btn = DropDownButton(text="Profile")
        profile_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "profile_screen"))
        profile_btn.bind(on_release=self.drop_down.dismiss)
        profile_btn.bind(on_release=lambda x: self.root.screen_manager.record())
        self.drop_down.add_widget(profile_btn)

        log_out_btn = DropDownButton(text="Log Out")
        log_out_btn.bind(on_release=lambda x: setattr(self.root.screen_manager,
                                                      "transition",
                                                      FadeTransition(clearcolor=(.8, .8, 1, 1))))
        log_out_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "login_screen"))
        log_out_btn.bind(on_release=lambda x: setattr(self.root.screen_manager,
                                                      "transition",
                                                      CardTransition(direction="down", mode="push")))
        log_out_btn.bind(on_release=self.drop_down.dismiss)
        self.drop_down.add_widget(log_out_btn)

        # open drop down when mouse is released on button
        self.bind(on_release=self.drop_down.open)


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
        if self.opacity != 1:
            return
        try:
            self.quantity += value
            Cart.item_action(self.name, value)
        except ValueError:
            return


class MainScrollView(ScrollView):
    pass


class ItemLayout(GridLayout):

    def __init__(self, **kwargs):
        super(ItemLayout, self).__init__(**kwargs)
        # dynamically add item views according to data file
        Item.start()  # start item class, load item data
        for item_info in Item.data:
            self.add_widget(ItemView(*item_info))

    def filter(self, text):

        # remove all children
        for _ in range(len(self.children)):
            self.remove_widget(self.children[0])

        # only add widget if pass filter
        for item_info in Item.data:
            name = item_info[0]
            item_view = ItemView(*item_info)
            if text.lower().replace(' ', '') in name.lower().replace(' ', ''):
                self.add_widget(item_view)

    def refresh(self):
        # load saved cart
        saved_cart = Cart.load_cart()
        for item_view in self.children:
            for name, info in saved_cart.items():
                if item_view.name == name:
                    item_view.quantity = info[1]
                    break
            else:
                item_view.quantity = 0
