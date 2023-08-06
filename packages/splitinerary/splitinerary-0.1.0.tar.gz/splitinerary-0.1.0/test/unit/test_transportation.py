from splitinerary import Transportation, Plane, Train, Boat, Car

import unittest
import datetime


class TestTransportation(unittest.TestCase):
    def test_create_object_success(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"
        # act
        transportation = Transportation(
            departure_time, arrival_time, cost, confirmation_code, now
        )
        # assert
        self.assertEqual(transportation.departure_time, departure_time)
        self.assertEqual(transportation.arrival_time, arrival_time)
        self.assertEqual(transportation.cost, cost)
        self.assertEqual(transportation.confirmation_code, confirmation_code)
        self.assertEqual(transportation.datetime, now)

    def test_str(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        date = str(now.date())
        time = str(now.time())
        expected_str = f"date: {date}, time: {time}, users: None, departure time: {departure_time}, arrival time: {arrival_time}"  # noqa
        # act
        transportation = Transportation(
            departure_time, arrival_time, cost, confirmation_code, now
        )
        # assert
        self.assertEqual(str(transportation), expected_str)


class TestPlane(unittest.TestCase):
    def test_create_object_success(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        flight_number = "NK 172"
        departure_terminal = "LGA"
        arrival_terminal = "DTW"
        # act
        plane = Plane(
            flight_number,
            departure_terminal,
            arrival_terminal,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(plane.departure_time, departure_time)
        self.assertEqual(plane.arrival_time, arrival_time)
        self.assertEqual(plane.cost, cost)
        self.assertEqual(plane.confirmation_code, confirmation_code)
        self.assertEqual(plane.datetime, now)

        self.assertEqual(plane.flight_number, flight_number)
        self.assertEqual(plane.departure_terminal, departure_terminal)
        self.assertEqual(plane.arrival_terminal, arrival_terminal)

    def test_str(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        date = str(now.date())
        time = str(now.time())

        flight_number = "NK 172"
        departure_terminal = "LGA"
        arrival_terminal = "DTW"

        expected_str = f"date: {date}, time: {time}, users: None, departure time: {departure_time}, arrival time: {arrival_time}, FLIGHT, flight_number: {flight_number}"  # noqa

        # act
        plane = Plane(
            flight_number,
            departure_terminal,
            arrival_terminal,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(str(plane), expected_str)


class TestTrain(unittest.TestCase):
    def test_create_object_success(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        train_line = "NEC"
        departure_station = "Penn Station, NYC"
        arrival_station = "Bernardsville, NJ"
        # act
        train = Train(
            departure_station,
            arrival_station,
            train_line,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(train.departure_time, departure_time)
        self.assertEqual(train.arrival_time, arrival_time)
        self.assertEqual(train.cost, cost)
        self.assertEqual(train.confirmation_code, confirmation_code)
        self.assertEqual(train.datetime, now)

        self.assertEqual(train.train_line, train_line)
        self.assertEqual(train.departure_station, departure_station)
        self.assertEqual(train.arrival_station, arrival_station)

    def test_str(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        date = str(now.date())
        time = str(now.time())

        train_line = "NEC"
        departure_station = "Penn Station, NYC"
        arrival_station = "Bernardsville, NJ"

        expected_str = f"date: {date}, time: {time}, users: None, departure time: {departure_time}, arrival time: {arrival_time}, TRAIN, departure_station: {departure_station}, arrival_station: {arrival_station}"  # noqa

        # act
        train = Train(
            departure_station,
            arrival_station,
            train_line,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(str(train), expected_str)


class TestBoat(unittest.TestCase):
    def test_create_object_success(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        departure_terminal = "Battery Park Dock 2"
        arrival_terminal = "Jersey City Slip 5"
        route = "Goldman Sachs Interoffice Ferry"
        # act
        boat = Boat(
            departure_terminal,
            arrival_terminal,
            route,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(boat.departure_time, departure_time)
        self.assertEqual(boat.arrival_time, arrival_time)
        self.assertEqual(boat.cost, cost)
        self.assertEqual(boat.confirmation_code, confirmation_code)
        self.assertEqual(boat.datetime, now)

        self.assertEqual(boat.departure_terminal, departure_terminal)
        self.assertEqual(boat.arrival_terminal, arrival_terminal)
        self.assertEqual(boat.route, route)

    def test_str(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        date = str(now.date())
        time = str(now.time())

        departure_terminal = "Battery Park Dock 2"
        arrival_terminal = "Jersey City Slip 5"
        route = "Goldman Sachs Interoffice Ferry"

        expected_str = f"date: {date}, time: {time}, users: None, departure time: {departure_time}, arrival time: {arrival_time}, BOAT, departure_terminal: {departure_terminal}, arrival_terminal: {arrival_terminal}"  # noqa

        # act
        boat = Boat(
            departure_terminal,
            arrival_terminal,
            route,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(str(boat), expected_str)


class TestCar(unittest.TestCase):
    def test_create_object_success(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        departure_location = "200 West St"
        arrival_location = "NYU Lafayette"
        company = "Lyft"
        # act
        car = Car(
            departure_location,
            arrival_location,
            company,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(car.departure_time, departure_time)
        self.assertEqual(car.arrival_time, arrival_time)
        self.assertEqual(car.cost, cost)
        self.assertEqual(car.confirmation_code, confirmation_code)
        self.assertEqual(car.datetime, now)

        self.assertEqual(car.departure_location, departure_location)
        self.assertEqual(car.arrival_location, arrival_location)
        self.assertEqual(car.company, company)

    def test_str(self):
        # arrange
        now = datetime.datetime.now()
        departure_time = "4:59"
        arrival_time = "7:07"
        cost = 41.84
        confirmation_code = "XB43MR"

        date = str(now.date())
        time = str(now.time())

        departure_location = "200 West St"
        arrival_location = "NYU Lafayette"
        company = "Lyft"

        expected_str = f"date: {date}, time: {time}, users: None, departure time: {departure_time}, arrival time: {arrival_time}, CAR, departure_location: {departure_location}, arrival_location: {arrival_location}"  # noqa

        # act
        car = Car(
            departure_location,
            arrival_location,
            company,
            departure_time=departure_time,
            arrival_time=arrival_time,
            cost=cost,
            confirmation_code=confirmation_code,
            datetime=now,
        )
        # assert
        self.assertEqual(str(car), expected_str)
