from cart import *

from os.path import isfile

from kivy.properties import BoundedNumericProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.gridlayout import GridLayout
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
        # profile_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "profile_screen"))
        profile_btn.bind(on_release=self.drop_down.dismiss)
        self.drop_down.add_widget(profile_btn)

        log_out_btn = DropDownButton(text="Log Out")
        log_out_btn.bind(on_release=lambda x: setattr(self.root.screen_manager, "current", "login_screen"))
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

        # recover all item view if search criteria is removed
        if not text.replace(' ', ''):
            for child in self.children:
                child.opacity = 1
                # re-enable plus and minus buttons for each item view
                child.plus_btn.disabled = False
                child.minus_btn.disabled = False
        else:
            for child in self.children:
                # filter according to whether search criteria is included in name or not
                if text.lower().replace(' ', '') in child.name.lower().replace(' ', ''):
                    child.opacity = 1
                    # re-enable plus and minus buttons if disabled
                    child.plus_btn.disabled = False
                    child.minus_btn.disabled = False

                else:
                    # temporarily disable plus and minus buttons
                    child.opacity = 0.2
                    child.plus_btn.disabled = True
                    child.minus_btn.disabled = True

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
