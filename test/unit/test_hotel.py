""" Unit tests for the Hotel class """
import io
import json
import unittest
import unittest.mock
from src.hotel import Hotel, HotelException
from src.customer import Customer
from src.reservation import ReservationException


class TestHotel(unittest.TestCase):
    """Test suite for Hotel functionality"""
    def setUp(self):
        """ Creates a hotel object and a db path for the tests """
        self.hotel = Hotel()
        self.db_path = 'hotels.json'

        # cleanup the file before the test
        with open(self.db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

    def tearDown(self):
        """Cleanup the file after the test"""
        with open(self.db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

    def test_hotel_gets_created(self):
        """ Test that a hotel gets created and persisted in file"""
        self.hotel.create('Hilton')

        stored_hotel = None
        with open(self.db_path, encoding='utf-8') as file:
            hotels = json.load(file)
            stored_hotel = hotels.get(self.hotel.id, None)

        self.assertIsNotNone(stored_hotel)
        self.assertEqual(stored_hotel.get('name'), 'Hilton')

    def test_hotel_gets_deleted(self):
        """Test that a hotel gets deleted from the file"""
        self.hotel.create('Hilton')
        self.hotel.delete()

        deleted_hotel = None
        with open(self.db_path, encoding='utf-8') as file:
            hotels = json.load(file)
            deleted_hotel = hotels.get(self.hotel.id, None)

        self.assertIsNone(deleted_hotel)

    def test_hotel_gets_modified(self):
        """Test that a hotel gets modified and persisted in file"""
        self.hotel.create('Hilton')
        self.hotel.modify_information('Fiesta Americana')

        modified_hotel = None
        with open(self.db_path, encoding='utf-8') as file:
            hotels = json.load(file)
            modified_hotel = hotels.get(self.hotel.id, None)

        self.assertIsNotNone(modified_hotel)
        self.assertEqual(modified_hotel.get('name'), 'Fiesta Americana')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_hotel_gets_displayed(self, mock_stdout):
        """Test that the hotel information gets displayed in console output"""
        self.hotel.create('Hilton')
        self.hotel.display_information()

        self.assertEqual(
            mock_stdout.getvalue(),
            f'Hotel ID: {self.hotel.id} \nHotel Name: Hilton \n\n'
        )

    def test_hotel_reserves_room(self):
        """
        Test that it is opssible to reserve a room
        given a customer in the current hotel
        """
        self.hotel.create('Hilton')

        customer = Customer()
        customer.create('Moises Diaz')

        self.hotel.reserve_room('101', customer)

        with open(self.db_path, encoding='utf-8') as file:
            hotels = json.load(file)
            reservations = hotels.get(self.hotel.id).get('reservations')

        self.assertIsNotNone(reservations)
        self.assertEqual(
            reservations.get('101').get('customer_id'),
            customer.id
        )

    def test_hotel_cancels_reservation(self):
        """
        Test that it is possible to cancel a reservation
        and that it gets removed from the db
        """
        self.hotel.create('Hilton')

        customer = Customer()
        customer.create('Moises Diaz')

        self.hotel.reserve_room('101', customer)
        self.hotel.cancel_reservation('101', customer)

        with open(self.db_path, encoding='utf-8') as file:
            hotels = json.load(file)
            reservations = hotels.get(self.hotel.id).get('reservations')

        self.assertEqual(reservations, {})

    def test_hotel_cancels_reservation_with_wrong_customer(self):
        """
        Test that it is not possible to cancel a reservation of
        a room with a different customer than the one that reserved it
        """
        self.hotel.create('Hilton')

        customer = Customer()
        customer.create('Moises Diaz')

        self.hotel.reserve_room('101', customer)

        customer2 = Customer()
        customer2.create('Moises Diaz Jr.')

        with self.assertRaises(ReservationException):
            self.hotel.cancel_reservation('101', customer2)

    def test_hotel_cancels_reservation_with_non_existing_reservation(self):
        """
        Test that it is not possible to cancel a reservation that
        does not exist.
        """
        self.hotel.create('Hilton')

        customer = Customer()
        customer.create('Moises Diaz')

        with self.assertRaises(ReservationException):
            self.hotel.cancel_reservation('101', customer)

    def test_hotel_found_by_id(self):
        """
        Test that a hotel is found by using its id given that it
        is stored in file.
        """
        self.hotel.create('Hilton')
        hotel = Hotel(self.hotel.id)

        self.assertEqual(hotel.name, 'Hilton')
        self.assertEqual(hotel.id, self.hotel.id)

    def test_hotel_not_found_raises_exception(self):
        """
        Test that an exception is raised when trying to find a
        non-existing hotel id in file.
        """
        with self.assertRaises(HotelException):
            _ = Hotel('123')

    def test_raises_exception_when_deleting_non_existing_hotel(self):
        """
        Test that an exception is raised when trying to delete a
        non-persisted hotel.
        """
        with self.assertRaises(HotelException):
            self.hotel.delete()
