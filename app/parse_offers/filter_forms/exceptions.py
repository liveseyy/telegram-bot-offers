class BadUserInputOption(Exception):
    def __init__(self, option_verbose_name, message="Wrong user input option in filter from"):
        self.option_verbose_name = option_verbose_name
        self.message = message
        super().__init__(self.message)
