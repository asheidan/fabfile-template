
class w:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __str__(self):
        return self()

    def replace(self, *args, **kwargs):
        return self().replace(*args, **kwargs)
