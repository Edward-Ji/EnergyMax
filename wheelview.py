from person import Person
from cart import Item

import pickle
from random import choice, randint, seed
import datetime

from loginview import show_popup

from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout

wheel_save_path = "save/wheel.p"


class WheelLayout(RelativeLayout):

    prize_index = ObjectProperty()
    available = BooleanProperty()
    shuffling = BooleanProperty(False)
    schedule = ObjectProperty()  # scheduled shuffle animation event
    name = StringProperty()
    img = StringProperty("wheel.png")

    def check(self):
        usr = Person.single.usr_id
        try:
            with open(wheel_save_path, 'br') as f:
                wheel_data = pickle.load(f)
                available_date = wheel_data[usr]
        except (FileNotFoundError, EOFError, KeyError):
            self.available = True
            return self.available
        self.available = datetime.date.today() >= available_date
        return self.available

    @staticmethod
    def save_status():

        # calculate next monday
        today = datetime.date.today()
        days_ahead = 1 - today.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        next_monday = today + datetime.timedelta(days_ahead)

        # save next available date to file
        usr = Person.single.usr_id
        try:
            with open(wheel_save_path, 'br') as f:
                wheel_data = pickle.load(f)
        except (FileNotFoundError, EOFError):
            wheel_data = {}
        wheel_data[usr] = next_monday
        with open(wheel_save_path, 'bw') as f:
            pickle.dump(wheel_data, f)

    def begin(self):

        # check if performed this week
        if not self.check():
            return

        # make it unavailable for this week
        self.available = False
        self.save_status()

        # schedule animation
        self.shuffling = True
        length = randint(3, 6)
        self.schedule = Clock.schedule_interval(self.shuffle, 0.1)
        Clock.schedule_once(lambda d_time: self.stop(), length)

    def shuffle(self, d_time):
        seed(d_time)
        not_chosen = list(range(0, len(Item.data) - 1))
        if self.prize_index:
            not_chosen.remove(self.prize_index)
        self.prize_index = choice(not_chosen)
        self.name, self.img, self.price = Item.data[self.prize_index]

    def stop(self):
        self.schedule.cancel()
        self.shuffling = False
        Person.single.earn_credits(1)
        show_popup("Congratulations!",
                   "You just got {}, which is worth ${:.2f}.\n"
                   "One credit earned for your account!".format(self.name.lower(), self.price))
