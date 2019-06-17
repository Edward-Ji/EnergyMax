class Cart:

    def __init__(self, person, item):
        self.person = person
        self.item = item

    def __repr__(self):
        return [self.person, self.item]
