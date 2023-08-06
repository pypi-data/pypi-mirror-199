from . import event


class CustomEvent(event.Event):
    def __init__(self, event_name, description, start_time, end_time, cost=0, *args, **kw):  # noqa
        self.event_name = event_name
        self.description = description
        self.cost = cost
        self.start_time = start_time
        self.end_time = end_time
        super().__init__(*args, **kw)

    def __str__(self) -> str:
        return (
            super().__str__()
            + f', Event name: {self.event_name}, Description: {self.description}, Start time: {self.start_time}, End time: {self.end_time}, Cost: {self.cost}'  # noqa
        )  # noqa

    def __eq__(self, other):
        return self.event_name == other.event_name and self.start_time == other.start_time  # noqa
