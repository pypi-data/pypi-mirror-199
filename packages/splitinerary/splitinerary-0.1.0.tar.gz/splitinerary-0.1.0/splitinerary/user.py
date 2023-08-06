class User:
    def __init__(self, first_name, last_name, email=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email  # assume that emails are unique to the user

    def get_email(self):
        return self.email

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}({self.email})'

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return self.email == other.email
