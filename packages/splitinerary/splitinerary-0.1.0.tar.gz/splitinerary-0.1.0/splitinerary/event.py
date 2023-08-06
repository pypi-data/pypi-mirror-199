class Event:
    """
    Event object. Sortable by datetime.

    Attributes:
        datetime: datetime.datetime object of when the user wants to arrive at
        the event, NOT NECESSARILY when the event starts (e.g. user might
        arrive at the airport 2 hours before the flight departs)
    """

    def __init__(self, datetime, users=None):
        self.datetime = datetime
        if users is None:
            self.users = []
        else:
            self.users = users

    def add_user(self, user):
        self.users.append(user)

    def get_users(self):
        return self.users if self.users else None

    def get_date(self):
        return self.datetime.date()

    def get_time(self):
        return self.datetime.time()

    def __lt__(self, other):
        return self.datetime < other.datetime

    def __eq__(self, other):
        return self.datetime == other.datetime

    def __str__(self) -> str:
        date = str(self.get_date())
        time = str(self.get_time())
        users = str(self.get_users())
        return f'date: {date}, time: {time}, users: {users}'
