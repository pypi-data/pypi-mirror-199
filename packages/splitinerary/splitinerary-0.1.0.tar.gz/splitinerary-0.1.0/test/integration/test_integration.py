import unittest
import datetime

from splitinerary import Plane, Boat, Train, Trip


class TestBasic(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.yesterday = self.now - datetime.timedelta(days=1)
        self.tomorrow = self.now + datetime.timedelta(days=1)

        my_departure_time = "16:59"
        my_arrival_time = "19:07"
        my_cost = 41.84
        my_confirmation_code = "XB43MR"

        my_flight_number = "NK 172"
        my_departure_terminal = "LGA"
        my_arrival_terminal = "DTW"

        self.my_flight = Plane(
            my_flight_number,
            my_departure_terminal,
            my_arrival_terminal,
            departure_time=my_departure_time,
            arrival_time=my_arrival_time,
            cost=my_cost,
            confirmation_code=my_confirmation_code,
            datetime=self.now,
        )

        alice_departure_time = "07:00"
        alice_arrival_time = "07:30"
        alice_cost = 15.99
        alice_confirmation_code = "ASL1209"

        alice_departure_terminal = "Battery Park Dock 2"
        alice_arrival_terminal = "Jersey City Slip 5"
        alice_route = "Goldman Sachs Interoffice Ferry"

        self.alice_boat = Boat(
            alice_departure_terminal,
            alice_arrival_terminal,
            alice_route,
            departure_time=alice_departure_time,
            arrival_time=alice_arrival_time,
            cost=alice_cost,
            confirmation_code=alice_confirmation_code,
            datetime=self.yesterday,
        )

        bob_departure_time = "12:26"
        bob_arrival_time = "13:26"
        bob_cost = 41.84
        bob_confirmation_code = "KJS2034"

        bob_train_line = "NEC"
        bob_departure_station = "Penn Station, NYC"
        bob_arrival_station = "Bernardsville, NJ"
        # act
        self.bob_train = Train(
            bob_departure_station,
            bob_arrival_station,
            bob_train_line,
            departure_time=bob_departure_time,
            arrival_time=bob_arrival_time,
            cost=bob_cost,
            confirmation_code=bob_confirmation_code,
            datetime=self.tomorrow,
        )

    def test_basic_trip(self):
        # arrange
        trip = Trip()

        # act
        trip.add_event(self.my_flight)
        trip.add_event(self.alice_boat)
        trip.add_event(self.bob_train)

        yesterdays_events = trip.get_events_on_date(self.yesterday.date())
        expected_yesterdays_events = [self.alice_boat]

        todays_events = trip.get_events_on_date(self.now.date())
        expected_todays_events = [self.my_flight]

        tomorrows_events = trip.get_events_on_date(self.tomorrow.date())
        expected_tomorrows_events = [self.bob_train]

        eventful_dates = trip.get_eventful_dates()
        expected_eventful_dates = [
            self.yesterday.date(),
            self.now.date(),
            self.tomorrow.date(),
        ]

        all_events = trip.get_all_events()
        expected_all_events = [self.alice_boat, self.my_flight, self.bob_train]

        next_event = trip.get_next_event()
        expected_next_event = self.bob_train

        # assert
        self.assertListEqual(yesterdays_events, expected_yesterdays_events)
        self.assertListEqual(todays_events, expected_todays_events)
        self.assertListEqual(tomorrows_events, expected_tomorrows_events)

        self.assertListEqual(eventful_dates, expected_eventful_dates)

        self.assertListEqual(all_events, expected_all_events)

        self.assertEqual(next_event, expected_next_event)
