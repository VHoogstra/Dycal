class BadLoginException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
        self.message = args[0]
