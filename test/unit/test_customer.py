"""Tests for Customer class functionality"""
import io
import json
import unittest
import unittest.mock
from src.customer import Customer, CustomerException


class TestCustomer(unittest.TestCase):
    """ Test suite for Customer functionality"""
    def setUp(self):
        self.customer = Customer()
        self.db_path = 'customers.json'

        # cleanup the file before the test
        with open(self.db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

    def tearDown(self):
        """Cleanup the file after the test"""
        with open(self.db_path, 'w', encoding='utf-8') as file:
            file.write('{}')

    def test_customer_gets_created(self):
        """Test that a customer gets created and persisted in file"""
        self.customer.create('Moises Diaz')

        created_customer = None
        with open(self.db_path, encoding='utf-8') as file:
            customers = json.load(file)
            created_customer = customers.get(self.customer.id, None)

        self.assertIsNotNone(created_customer)
        self.assertEqual(created_customer.get('name'), 'Moises Diaz')

    def test_customer_gets_deleted(self):
        """Test that a customer gets deleted from the file"""
        self.customer.create('Moises Diaz')
        self.customer.delete()

        deleted_customer = None
        with open(self.db_path, encoding='utf-8') as file:
            customers = json.load(file)
            deleted_customer = customers.get(self.customer.id, None)

        self.assertIsNone(deleted_customer)

    def test_customer_gets_modified(self):
        """Test that a customer gets modified and persisted in file"""
        self.customer.create('Moises Diaz')
        self.customer.modify_information('Moises Diaz Jr.')

        modified_customer = None
        with open(self.db_path, encoding='utf-8') as file:
            customers = json.load(file)
            modified_customer = customers.get(self.customer.id, None)

        self.assertIsNotNone(modified_customer)
        self.assertEqual(modified_customer.get('name'), 'Moises Diaz Jr.')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_customer_gets_displayed(self, mock_stdout):
        """Test that a customer gets displayed in console output"""
        self.customer.create('Moises Diaz')
        self.customer.display_information()

        self.assertEqual(
            mock_stdout.getvalue(),
            (f'Customer ID: {self.customer.id} \n'
             f'Customer Name: Moises Diaz \n\n')
        )

    def test_customer_not_found(self):
        """Test that a customer not found raises an exception"""
        with self.assertRaises(CustomerException):
            _ = Customer('123')

    def test_customer_found_by_id(self):
        """Test that a customer is found by id"""
        self.customer.create('Moises Diaz')
        customer = Customer(self.customer.id)

        self.assertEqual(customer.name, 'Moises Diaz')
        self.assertEqual(customer.id, self.customer.id)

    def test_raises_exception_when_deleting_non_existing_customer(self):
        """Test that deleting a non-existing customer raises an exception"""
        with self.assertRaises(CustomerException):
            self.customer.delete()
