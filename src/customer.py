"""Module for Customer class"""
import uuid
import json


class CustomerException(Exception):
    """
    Custom exception for Customer class
    """


class Customer:
    """Class for Customer"""
    DB_PATH = 'customers.json'

    def __init__(self, id_=None):

        if id_:
            self.id = id_
            existing_customer = self._find()
            if existing_customer is None:
                raise CustomerException('Customer not found')
            self.name = existing_customer.get('name')

        else:
            self.id = str(uuid.uuid4())
            self.name = None

    def create(self, name):
        """
        Stores the customer in the DB

        Args:
            name (str): The name of the customer

        Returns:
            None
        """
        self.name = name
        self._save()

    def delete(self):
        """
        Deletes the current customer from the DB

        Returns:
            None
        """
        with open(self.DB_PATH, 'r+', encoding='utf-8') as file:
            customers = json.load(file)

            exists = customers.get(self.id)
            if not exists:
                raise CustomerException('Customer is not stored in db')

            del customers[self.id]
            file.seek(0)
            json.dump(customers, file)
            file.truncate()

    def display_information(self):
        """
        Prints the information of the customer

        Returns:
            None
        """
        print(f'Customer ID: {self.id} \nCustomer Name: {self.name} \n')

    def modify_information(self, name):
        """
        Updates the name of the customer

        Args:
            name (str): The new name of the customer

        Returns:
            None
        """
        self.name = name
        # persist the changes
        self._save()

    def _find(self):
        """
        Finds and returns the customer in the DB given the current object id

        Returns:
            dict: The customer information
        """
        with open(self.DB_PATH, encoding='utf-8') as file:
            customers = json.load(file)
            return customers.get(self.id, None)

    def _save(self):
        """
        Saves the current customer information in the DB

        Returns:
            None

        """
        with open(self.DB_PATH, 'r+', encoding='utf-8') as file:
            customers = json.load(file)
            customers[self.id] = {
                'name': self.name
            }
            file.seek(0)
            json.dump(customers, file)
            file.truncate()
