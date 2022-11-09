class InvalidOptions(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"InvalidOptions: {message}")
        self.message = message