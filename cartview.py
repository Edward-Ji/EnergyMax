from cart import *

from loginview import show_popup
from mainview import ToolBarButton, MainButton

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class HelpButton(ToolBarButton):

    def on_release(self):
        show_popup("Information", self.msg)


class CartTitle(BoxLayout):
    pass


class CartItem(BoxLayout):

    def __init__(self, name, price, quantity, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.name = name
        self.price = price
        self.quantity = quantity


class CartLayout(BoxLayout):

    def refresh(self):
        self.clear_widgets()
        if Cart.content:
            self.add_widget(CartTitle())
            for name, info in Cart.content.items():
                self.add_widget(CartItem(name, *info))
            if self.pay_button is not None:
                self.pay_button.disabled = False
        else:
            self.add_widget(Label(text="There is not item in your cart yet!",
                                  color=(0, 0, 0, 1),
                                  font_size=18))
            self.pay_button.disabled = True
        if self.status_bar is not None:
            self.status_bar.total, self.status_bar.discount, self.status_bar.payment = Cart.status()


class PayButton(MainButton):

    def on_release(self):

        if not Person.single.cards:  # check if user has any bank cards
            show_popup("Payment method not found", "You have not set up any payment method.\n"
                                                   "Bind a bank card to continue. ")
            self.root.screen_manager.record()
            self.root.screen_manager.current = "profile_screen"
        else:
            # select bank card popup
            pop_layout = BoxLayout(orientation="vertical",
                                   padding=3,
                                   spacing=10)
            card_popup = Popup(title="Pay using...",
                               content=pop_layout,
                               size_hint=(.5, .5))
            for card_num, _ in Person.single.cards:
                card_btn = MainButton(text=card_num,
                                      size_hint=(.8, None),
                                      height=44,
                                      pos_hint={"center_x": .5})
                pop_layout.add_widget(card_btn)
                card_btn.bind(on_release=lambda _: self.receipt(card_num))
                card_btn.bind(on_release=card_popup.dismiss)
            close_btn = Button(text="Close",
                               size_hint=(None, None),
                               size=(85, 50),
                               pos_hint={"center_x": .5})
            pop_layout.add_widget(close_btn)
            close_btn.bind(on_release=card_popup.dismiss)
            card_popup.open()

    def receipt(self, card_num):
        receipt = self.root.screen_manager.receipt_screen.receipt
        receipt.card_num = card_num
        receipt.pay_info = Cart.status()
        self.root.screen_manager.current = "receipt_screen"
        Cart.clear_cart()
