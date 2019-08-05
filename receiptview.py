from person import *
from settings import *

import datetime
import os
from loginview import show_popup

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


class ReceiptPair(BoxLayout):

    def __init__(self, **kwargs):
        self.key = kwargs.pop("key")
        self.val = kwargs.pop("val")
        super(ReceiptPair, self).__init__(**kwargs)


class ReceiptLayout(BoxLayout):

    path = StringProperty()
    serial = StringProperty()

    def refresh(self):

        # allocate a serial number
        today = datetime.datetime.today().strftime("%y%m%d")
        last_date, count = Settings.retrieve("serial", (today, 0))
        if last_date != today:
            count = 1
        else:
            count += 1
        Settings.push("serial", (today, count))
        self.serial = today + str(count).rjust(5, '0')

        # display user and shop detail on receipt
        info = {"User": Person.single.usr_id, "Serial number": self.serial,
                "Time": datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
                "Payment method": self.card_num,
                "Net total": "${:.2f}".format(self.pay_info[0]),
                "Discount": "${:.2f}".format(self.pay_info[1]),
                "Payment": "${:.2f}".format(self.pay_info[2])}
        for key, val in info.items():
            self.add_widget(ReceiptPair(key=key, val=val))

        # save transaction
        with open("save/transactions.txt", 'a') as f:
            f.write("<--- Purchase Details --->\n")
            for key, value in info.items():
                f.write("{:18s}|{}\n".format(key, value))
            f.write("\n=*=*=*=*=*=*=*=*=*=\n")

        # export receipt as png
        self.path = os.path.abspath("receipts/{}.png".format(self.serial))
        Clock.schedule_once(lambda _: self.export_to_png(self.path))  # export as soon as widget is rendered net frame
