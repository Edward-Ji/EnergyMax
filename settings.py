import pickle

SETTINGS_SAVE = "save/settings.p"


class Settings:

    single = None

    def __init__(self):
        try:
            with open(SETTINGS_SAVE, 'br') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}
            f = open(SETTINGS_SAVE, 'bw')
            pickle.dump(self.data, f)
            f.close()

    @classmethod
    def start(cls):
        if cls.single:
            raise ValueError("Setting management instance exists")
        else:
            cls.single = Settings()

    @classmethod
    def push(cls, key, value):
        cls.single.data[key] = value
        with open(SETTINGS_SAVE, 'bw') as f:
            pickle.dump(cls.single.data, f)

    @classmethod
    def retrieve(cls, key, default):
        return cls.single.data.get(key, default)
