from person import *

import pickle

ITEM_RES = "res/items.p"
CART_SAVE = "save/cart.p"


class Item:

    data = None

    @classmethod
    def get_price(cls, name):
        for item in cls.data:
            if name == item[0]:
                return item[2]

    @classmethod
    def start(cls):
        with open(ITEM_RES, 'br') as f:
            cls.data = pickle.load(f)


class Cart:

    content = {}

    @classmethod
    def item_action(cls, name, value):
        if cls.content.get(name):
            price, quantity = cls.content.get(name)
            quantity += value
            if quantity == 0:
                del cls.content[name]
                cls.save_cart()
                return
        else:
            price = Item.get_price(name)
            quantity = 1
        cls.content[name] = price, quantity
        cls.save_cart()

    @classmethod
    def load_cart(cls):
        usr = Person.single.usr_id
        try:
            with open(CART_SAVE, 'br') as f:
                cart_save = pickle.load(f)
                cls.content = cart_save.get(usr, {})
        except (FileNotFoundError, EOFError):
            cls.content = {}
        return cls.content

    @classmethod
    def save_cart(cls):
        usr = Person.single.usr_id
        try:
            with open(CART_SAVE, 'br') as f:
                cart_save = pickle.load(f)
        except (FileNotFoundError, EOFError):
            cart_save = {}
        cart_save[usr] = cls.content
        with open(CART_SAVE, 'bw') as f:
            pickle.dump(cart_save, f)

    @classmethod
    def status(cls):
        total = 0
        discount = 0
        for name, info in cls.content.items():
            price, quantity = info
            total += price * quantity
        if total >= 250:
            discount = 0.1 * total
        payment = total - discount
        return total, discount, payment

    @classmethod
    def clear_cart(cls):
        cls.content = {}
        cls.save_cart()
