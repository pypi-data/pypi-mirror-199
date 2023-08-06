from splitinerary import Event, User

import unittest
import datetime


class TestEvent(unittest.TestCase):
    def test_create_event_with_user_success(self):
        # arrange
        now = datetime.datetime.now()
        users = [
            User('Tim', "Paine", "tim@columbia.edu"),
            User('Catelen', "Wu", "Catelen@columbia.edu")
            ]
        # act
        event = Event(now, users)
        # assert
        self.assertListEqual(event.users, users)

    def test_add_user_to_event_success(self):
        # arrange
        now = datetime.datetime.now()
        event = Event(now)
        user = User('Tim', "Paine", "tim@columbia.edu")
        # act
        event.add_user(user)
        # assert
        self.assertListEqual(event.users, [user])
