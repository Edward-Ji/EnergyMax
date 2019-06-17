import pickle


TRANSACTIONS = "save/transactions.p"


class Transaction:

    carts = None

    def __init__(self, carts):
        self.carts = carts
        self.price = None

    def pay(self, cash):
        self.price = self.get_discount_price()
        self.receipt(cash)
        self.save()

    def get_raw_price(self):
        price_sum = 0
        for cart in self.carts:
            price_sum += cart.item.price
        return price_sum

    def get_discount_price(self):
        discount_price = self.get_raw_price()
        if discount_price >= 250:
            discount_price *= 0.9
        else:
            discount_price *= 0.95
        return discount_price

    def receipt(self, cash):
        # todo: show receipt
        print("Show receipt", self.price, cash)

    def save(self):
        try:
            transactions = pickle.load(open(TRANSACTIONS, 'br'))
        except FileNotFoundError:
            transactions = []
        transactions.append(self.carts)
        pickle.dump(transactions, open(TRANSACTIONS, 'bw'))
