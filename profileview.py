from person import *

import datetime
import re

from loginview import show_popup
from mainview import MainButton

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout

card_number_pattern = r"[\d]{16}$"
card_exp_date_pattern = r"[\d]{2}$"


# profile settings under change password subject
class ChangePswBtn(MainButton):

    def on_release(self):
        ori_psw, new_psw = self.ori_psw.text, self.new_psw.text
        msg = Person.single.change_psw(ori_psw, new_psw)
        if msg:
            show_popup("Request failed", msg)
        else:
            # clear password to prevent breach
            self.ori_psw.psw_input.text = ''
            self.new_psw.psw_input.text = ''
            # return back to login screen
            show_popup("Congratulations",
                       "You successfully changed your password!\n"
                       "Re-login to continue!")
            self.root.screen_manager.current = "login_screen"


# profile settings under cards subject
class AddCardLayout(BoxLayout):

    default_color = 0, 0, 0, 0.1
    invalid_color = 1, 0.4, 0.4, 1

    def add(self):

        error_msg = []

        # check card number syntax
        card_number = self.card_number.text
        if not re.match(card_number_pattern, card_number):
            self.card_number.background_color = self.invalid_color
            error_msg.append("Card number should be a 16-digit number.")
        else:
            self.card_number.background_color = self.default_color

        # check expiry date syntax
        exp_date_error = False
        for field in self.exp_date:
            if not re.match(card_exp_date_pattern, field.text):
                field.background_color = self.invalid_color
                exp_date_error = True
            else:
                field.background_color = self.default_color

        # more advanced check no expiry date
        if not exp_date_error:  # if passed simple test on expiry date
            exp_day = int(self.exp_day.text)
            exp_month = int(self.exp_month.text)
            exp_year = int('20' + self.exp_year.text)
            try:
                exp_date = datetime.date(day=exp_day, month=exp_month, year=exp_year)  # check if date is valid
                if datetime.date.today() > exp_date:  # check if date is in the past
                    error_msg.append("Expiry date can not be in the past.")
                    field_color = self.invalid_color
                else:
                    field_color = self.default_color
            except ValueError:
                field_color = self.invalid_color
                error_msg.append("The expiry date you entered is not valid.")
            for field in self.exp_date:
                field.background_color = field_color
        else:
            error_msg.append("The expiry date you entered is not valid.")

        # add card plus logic check
        if not error_msg:
            card_exp_date = '/'.join(map(str, (exp_day, exp_month, exp_year)))
            msg = Person.single.add_card(card_number, card_exp_date)
            if msg:
                error_msg.append(msg)

        # if there is an error popup error message
        if error_msg:
            show_popup("Request failed", '\n'.join(error_msg))
        else:
            # clear field and refresh card layout to show card(s)
            self.card_number.text = ''
            for field in self.exp_date:
                field.text = ''
            self.card_layout.refresh()
            show_popup("Congratulations!",
                       "Bank card is successfully added.\n"
                       "You can now use it to pay.\n"
                       "Go and enjoy shopping now!")


class CardNumberLabel(Label):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.text = self.root.number

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            self.text = self.root.number_hint

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.text = self.root.number_hint


class CardItem(RelativeLayout):

    def __init__(self, number, exp_date, **kwargs):
        super(CardItem, self).__init__(**kwargs)
        self.number = ' '.join([number[4*i:4*i+4] for i in range(4)])
        self.number_hint = "**** **** **** " + self.number[-4:]
        self.exp_date = exp_date

    def remove(self):
        number = self.number.replace(' ', '')
        index = Person.single.cards.index((number, self.exp_date))

        show_popup("Warning",
                   "Are you sure you want to remove the card permanently?\n"
                   "This operation can not be undone!",
                   "Confirm",
                   (lambda d_time: self.parent.refresh(),
                    lambda d_time: Person.single.remove_card(index)))


class CardLayout(BoxLayout):

    def refresh(self):
        self.clear_widgets()
        for number, exp_date in Person.single.cards:
            self.add_widget(CardItem(number, exp_date))
