from cart import Cart

from mainview import ToolBar, ToolBarButton, MainButton, MainScrollView

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class MainLabel(Label):
    pass


class CartItem(BoxLayout):

    def __init__(self, name, price, quantity, **kwargs):
        super(CartItem, self).__init__(**kwargs)
        self.name = name
        self.price = price
        self.quantity = quantity


class CartLayout(BoxLayout):

    def refresh(self):
        for widget in self.children:
            self.remove_widget(widget)
        if Cart.content:
            for name, info in Cart.content.items():
                self.add_widget(CartItem(name, *info))
            self.pay_button.disabled = False
        else:
            self.add_widget(MainLabel(text="There is not item in your cart yet!"))
            self.pay_button.disabled = True
        self.status_bar.total, self.status_bar.discount, self.status_bar.payment = Cart.status()


class PayButton(MainButton):

    def on_release(self):
        pass
        # self.receipt.export_to_png("receipt.png")
