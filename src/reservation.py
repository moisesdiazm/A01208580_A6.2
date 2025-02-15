"""Module for Reservation class"""
import json


class ReservationException(Exception):
    """
    Custom exception for Reservation class
    """


class Reservation:
    """Class for Reservation"""
    DB_PATH = 'hotels.json'

    def __init__(self, room_number, hotel_id, customer_id):
        self.room_number = str(room_number)
        self.hotel_id = hotel_id
        self.customer_id = customer_id

    def create(self):
        """Create a reservation for a room

        Returns:
            None
        """
        # check if the room is available
        if self._find_reservation():
            raise ReservationException('Room is already reserved')

        # add reservation
        with open('hotels.json', 'r+', encoding='utf-8') as file:
            hotels = json.load(file)
            if not hotels.get(self.hotel_id).get('reservations'):
                hotels[self.hotel_id]['reservations'] = {}

            hotels[self.hotel_id]['reservations'][self.room_number] = {
                'customer_id': self.customer_id
            }
            file.seek(0)
            json.dump(hotels, file)
            file.truncate()

    def cancel(self):
        """
        Cancel a reservation

        Returns:
            None
        """
        with open('hotels.json', 'r+', encoding='utf-8') as file:
            hotels = json.load(file)

            existing_reservation = self._find_reservation()
            if not existing_reservation:
                raise ReservationException('Reservation not found')

            if existing_reservation.get('customer_id') != self.customer_id:
                raise ReservationException('Customer ID does not match, '
                                           'cannot cancel reservation')

            del hotels[self.hotel_id]['reservations'][self.room_number]
            file.seek(0)
            json.dump(hotels, file)
            file.truncate()

    def _find_reservation(self):
        """
        Private method to find a reservation given a hotel_id and room_number

        Returns:
            dict: Reservation details
        """

        with open('hotels.json', 'r+', encoding='utf-8') as file:
            hotels = json.load(file)

            existing_hotel = hotels.get(self.hotel_id)

            if not existing_hotel:
                raise ReservationException('Hotel not found')

            reservations = existing_hotel.get('reservations')

            if not reservations:
                return None

            return reservations.get(self.room_number, None)
