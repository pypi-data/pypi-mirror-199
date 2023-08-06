from splitinerary import Event, Trip, User

import unittest
import datetime


class TestAddEvent(unittest.TestCase):
    def test_add_event_without_user_success(self):
        # arrange
        now = datetime.datetime.now()
        date = now.date()
        trip = Trip()
        event = Event(now)

        expected_dates_list = [date]
        expected_dates_dict = {date: [event]}

        # act
        trip.add_event(event)

        # assert
        self.assertListEqual(trip.dates_list, expected_dates_list)
        self.assertDictEqual(trip.dates_dict, expected_dates_dict)

    def test_add_event_with_user_success(self):
        # arrange
        now = datetime.datetime.now()
        date = now.date()
        trip = Trip()
        user = User('tim', 'paine', 'tim@columbia.edu')
        event = Event(now, [user])

        expected_dates_list = [date]
        expected_dates_dict = {date: [event]}
        expected_user_activities = {user: {date: [event]}}

        # act
        trip.add_event(event)

        # assert
        self.assertListEqual(trip.dates_list, expected_dates_list)
        self.assertDictEqual(trip.dates_dict, expected_dates_dict)
        self.assertDictEqual(trip.user_activities, expected_user_activities)


class TestGetEventsOnDate(unittest.TestCase):
    def test_get_events_on_eventful_date_success(self):
        # arrange
        now = datetime.datetime.now()
        date = now.date()
        trip = Trip()
        event = Event(now)
        trip.add_event(event)
        expected_events_list = [event]

        # act
        events = trip.get_events_on_date(date)

        # assert
        self.assertListEqual(events, expected_events_list)

    def test_get_events_on_uneventful_date_success(self):
        # arrange
        now = datetime.datetime.now()
        date = now.date()
        trip = Trip()

        # act
        events = trip.get_events_on_date(date)

        # assert
        self.assertIsNone(events)


class TestGetEventfulDates(unittest.TestCase):
    def test_get_eventful_dates_success(self):
        # arrange
        now = datetime.datetime.now()
        date = now.date()
        trip = Trip()
        event = Event(now)
        trip.add_event(event)
        expected_dates_list = [date]

        # act
        dates = trip.get_eventful_dates()

        # assert
        self.assertListEqual(dates, expected_dates_list)

    def test_get_no_eventful_dates_success(self):
        # arrange
        trip = Trip()

        # act
        dates = trip.get_eventful_dates()

        # assert
        self.assertIsNone(dates)


class TestGetAllEvents(unittest.TestCase):
    def test_get_all_events_success(self):
        # arrange
        now = datetime.datetime.now()
        trip = Trip()
        event = Event(now)
        trip.add_event(event)
        expected_events_list = [event]

        # act
        events = trip.get_all_events()

        # assert
        self.assertListEqual(events, expected_events_list)

    def test_get_no_events_success(self):
        # arrange
        trip = Trip()

        # act
        events = trip.get_all_events()

        # assert
        self.assertIsNone(events)


class TestGetNextEvent(unittest.TestCase):
    def test_get_next_event_success(self):
        # arrange
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        yesterday = now - datetime.timedelta(days=1)
        trip = Trip()
        yesterdayss_event = Event(yesterday)
        tomorrows_event = Event(tomorrow)
        trip.add_event(yesterdayss_event)
        trip.add_event(tomorrows_event)

        # act
        next_event = trip.get_next_event()

        # assert
        self.assertEqual(next_event, tomorrows_event)

    def test_get_next_event_after_lastsuccess(self):
        # arrange
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        trip = Trip()
        yesterdayss_event = Event(yesterday)
        trip.add_event(yesterdayss_event)

        # act
        next_event = trip.get_next_event()

        # assert
        self.assertIsNone(next_event)


class TestGetUsersList(unittest.TestCase):
    def test_get_users_list_success(self):
        # arrange
        now = datetime.datetime.now()

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])
        user2 = User('catelen', 'wu', 'catelen@columbia.edu')
        event2 = Event(now, [user2])

        trip = Trip()
        trip.add_event(event1)
        trip.add_event(event2)

        expected_users_list = [user1, user2]

        # act
        users_list = trip.get_users_list()

        # assert
        self.assertListEqual(users_list, expected_users_list)


class TestGetEventsOfUser(unittest.TestCase):
    def test_get_events_of_user_success(self):
        # arrange
        now = datetime.datetime.now()

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])
        user2 = User('catelen', 'wu', 'catelen@columbia.edu')
        event2 = Event(now, [user2])

        trip = Trip()
        trip.add_event(event1)
        trip.add_event(event2)

        # act
        events_of_user = trip.get_events_of_user(user1)

        # assert
        self.assertDictEqual(events_of_user, {now.date(): [event1]})

    def test_get_events_of_unknown_user_success(self):
        # arrange
        now = datetime.datetime.now()

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])
        user2 = User('catelen', 'wu', 'catelen@columbia.edu')

        trip = Trip()
        trip.add_event(event1)

        # act
        events_of_user = trip.get_events_of_user(user2)

        # assert
        self.assertIsNone(events_of_user)


class TestRemoveEventByIndex(unittest.TestCase):
    def test_remove_event_by_index_success(self):
        # arrange
        now = datetime.datetime.now()
        next_second = now + datetime.timedelta(seconds=1)

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])
        event2 = Event(next_second, [user1])

        trip = Trip()
        trip.add_event(event1)
        trip.add_event(event2)

        # act
        trip.remove_event_by_index(now.date(), 1)

        # assert
        todays_events = trip.get_events_on_date(now.date())
        self.assertEqual(todays_events, [event1])

    def test_remove_event_by_index_nonexistent_date_success(self):
        # arrange
        now = datetime.datetime.now()
        next_second = now + datetime.timedelta(seconds=1)
        tomorrow = now + datetime.timedelta(days=1)

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])
        event2 = Event(next_second, [user1])

        trip = Trip()
        trip.add_event(event1)
        trip.add_event(event2)

        # act
        trip.remove_event_by_index(tomorrow, 1)

        # assert
        todays_events = trip.get_events_on_date(now.date())
        self.assertEqual(todays_events, [event1, event2])

    def test_remove_event_by_index_nonexistent_index_success(self):
        # arrange
        now = datetime.datetime.now()
        next_second = now + datetime.timedelta(seconds=1)

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])
        event2 = Event(next_second, [user1])

        trip = Trip()
        trip.add_event(event1)
        trip.add_event(event2)

        # act
        trip.remove_event_by_index(now.date(), 2)

        # assert
        todays_events = trip.get_events_on_date(now.date())
        self.assertEqual(todays_events, [event1, event2])

    def test_remove_event_by_index_last_event_on_date_success(self):
        # arrange
        now = datetime.datetime.now()

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        event1 = Event(now, [user1])

        trip = Trip()
        trip.add_event(event1)

        # act
        trip.remove_event_by_index(now.date(), 0)

        # assert
        self.assertEqual(len(trip.dates_list), 0)


class TestRemoveUserFromEvent(unittest.TestCase):
    def test_remove_user_from_event_success(self):
        # arrange
        now = datetime.datetime.now()

        user1 = User('tim', 'paine', 'tim@columbia.edu')
        user2 = User('catelen', 'wu', 'catelen@columbia.edu')
        event1 = Event(now, [user1, user2])

        trip = Trip()
        trip.add_event(event1)

        # act
        trip.remove_user_from_event(user1, event1)

        # assert
        event_participants = event1.get_users()
        self.assertListEqual(event_participants, [user2])
