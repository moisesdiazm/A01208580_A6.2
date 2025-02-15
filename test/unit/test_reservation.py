"""Test suite for Reservation"""
import unittest
from src.reservation import Reservation
from src.hotel import Hotel
from src.customer import Customer


class TestReservation(unittest.TestCase):
    """
    Test suite for Reservation not tested in hotel functionality
    e.g. reserving a room in a non-existing hotel.
    """

    def setUp(self):
        """
        Setup the test

        Returns:
            None
        """
        self.hotels_db_path = 'hotels.json'
        self.customers_db_path = 'customers.json'

        # cleanup the file before the test
        with open(self.hotels_db_path, 'w', encoding='utf-8') as file:
            file.write('{}')
        with open(self.customers_db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

        self.hotel = Hotel()
        self.hotel.create("Hilton")
        self.customer = Customer()
        self.customer.create("Moises Diaz")

    def tearDown(self):
        """Cleanup the file after the test"""
        with open(self.hotels_db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

        with open(self.customers_db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

    def test_room_already_reserved_raises_exception(self):
        """
        Test that reserving a room that is already reserved
        raises an exception.
        """
        self.hotel.reserve_room('101', self.customer)

        with self.assertRaises(Exception):
            reservation = Reservation('101', self.hotel.id, self.customer.id)
            reservation.create()

    def test_non_existing_hotel_raises_exception(self):
        """
        Test that reserving a room in a non-existing hotel
        raises an exception.
        """
        with self.assertRaises(Exception):
            reservation = Reservation(
                '101',
                'non-existing-hotel',
                self.customer.id
            )
            reservation.create()
