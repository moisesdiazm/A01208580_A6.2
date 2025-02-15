"""Module for Hotel class"""
import uuid
import json
from src.reservation import Reservation


class HotelException(Exception):
    """
    Custom exception for Hotel class
    """


class Hotel:
    """Class for Hotel"""
    DB_PATH = 'hotels.json'

    def __init__(self, id_=None):
        if id_:
            self.id = id_
            existing_hotel = self._find()
            if existing_hotel is None:
                raise HotelException('Hotel not found')

            self.name = existing_hotel.get('name')

        else:
            self.id = str(uuid.uuid4())
            self.name = None

    def create(self, name):
        """
        Stores the hotel in the DB

        Args:
            name (str): The name of the hotel

        Returns:
            None
        """
        self.modify_information(name)

    def delete(self):
        """
        Removes the current hotel from the DB

        Returns:
            None

        """
        with open(self.DB_PATH, 'r+', encoding='utf-8') as file:
            hotels = json.load(file)

            exists = hotels.get(self.id)
            if not exists:
                raise HotelException('Hotel is not stored in db')

            del hotels[self.id]
            file.seek(0)
            json.dump(hotels, file)
            file.truncate()

    def display_information(self):
        """
        Prints the information of the hotel

        Returns:
            None

        """
        print(f'Hotel ID: {self.id} \nHotel Name: {self.name} \n')

    def modify_information(self, name):
        """
        Modify the name of the hotel

        Args:
            name (str): The new name of the hotel

        Returns:
            None
        """
        self.name = name
        self._save()

    def reserve_room(self, room_number, customer):
        """
        Allows a customer to reserve a room, given a room number and a customer

        Args:
            room_number (str): The room number
            customer (Customer): The customer object

        Returns:
            None

        """
        # reserve the room
        reservation = Reservation(
            room_number=room_number,
            hotel_id=self.id,
            customer_id=customer.id
        )
        reservation.create()

    def cancel_reservation(self, room, customer):
        """
        Cancels a reservation given a room number and a customer

        Args:
            room (str): The room number
            customer (Customer): The customer object

        Returns:
            None
        """
        reservation = Reservation(
            room_number=room,
            hotel_id=self.id,
            customer_id=customer.id
        )
        reservation.cancel()
        del reservation

    def _find(self):
        """
        Private method to find a hotel in the DB given the current object id

        Returns:
            dict: Hotel details

        """
        with open('hotels.json', encoding='utf-8') as file:
            hotels = json.load(file)
            return hotels.get(self.id)

    def _save(self):
        """
        Saves the current hotel information in the DB

        Returns:
            None

        """
        with open('hotels.json', 'r+', encoding='utf-8') as file:
            hotels = json.load(file)
            hotels[self.id] = {
                'id': self.id,
                'name': self.name
            }
            file.seek(0)
            json.dump(hotels, file)
            file.truncate()
