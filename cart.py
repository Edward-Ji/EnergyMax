class Cart:

    family = []

    def __init__(self, person, item):
        self.person = person
        self.item = item
        self.family.append(self)

    def __repr__(self):
        return [self.person, self.item]
