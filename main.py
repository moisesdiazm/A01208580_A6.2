"""Main module to demonstrate an usage example"""

from src.customer import Customer
from src.hotel import Hotel


def main():
    """Main function to demonstrate an example usage of the classes"""

    h1 = Hotel()
    h1.create('Fiesta Americana')
    h1.display_information()
    h1.modify_information("Hilton")

    c1 = Customer()
    c1.create("Mdiaz Malagon")
    c1.display_information()

    h1.reserve_room(231, customer=c1)

    # h1.cancel_reservation(231, customer=c1)

    # h1.delete()
    # c1.delete()


if __name__ == '__main__':
    main()
