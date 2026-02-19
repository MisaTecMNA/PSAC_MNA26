import unittest
import os
import json
from hotel_system import Hotel, Customer, Reservation, FileManager

class TestHotelSystem(unittest.TestCase):
    """
    Suite de Pruebas Completa: Escenarios Positivos y Negativos.
    """

    def setUp(self):
        """Restablece los archivos JSON a un estado limpio antes de CADA prueba."""
        self.hotels_file = FileManager.get_filepath('hotels.json')
        self.customers_file = FileManager.get_filepath('customers.json')
        self.reservations_file = FileManager.get_filepath('reservations.json')

        with open(self.hotels_file, 'w') as f: json.dump([], f)
        with open(self.customers_file, 'w') as f: json.dump([], f)
        with open(self.reservations_file, 'w') as f: json.dump([], f)

    # ==========================================
    # CASOS POSITIVOS (Camino Feliz)
    # ==========================================

    def test_hotel_operations_positive(self):
        """Positivo: Crear, Leer, Actualizar y Eliminar un Hotel."""
        # 1. Crear
        Hotel.create_hotel("H1", "Plaza", "CDMX", 10)
        hotel = Hotel.display_hotel_info("H1")
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel['name'], "Plaza")

        # 2. Actualizar
        Hotel.modify_hotel_info("H1", name="Plaza Central", rooms=15)
        hotel_updated = Hotel.display_hotel_info("H1")
        self.assertEqual(hotel_updated['name'], "Plaza Central")
        self.assertEqual(hotel_updated['rooms'], 15)

        # 3. Eliminar
        Hotel.delete_hotel("H1")
        hotel_deleted = Hotel.display_hotel_info("H1")
        self.assertIsNone(hotel_deleted)

    def test_customer_operations_positive(self):
        """Positivo: Crear, Leer, Actualizar y Eliminar un Cliente."""
        # 1. Crear
        Customer.create_customer("C1", "Carlos", "carlos@mail.com")
        cust = Customer.display_customer_info("C1")
        self.assertIsNotNone(cust)
        self.assertEqual(cust['name'], "Carlos")

        # 2. Actualizar
        Customer.modify_customer_info("C1", email="carlos_nuevo@mail.com")
        cust_updated = Customer.display_customer_info("C1")
        self.assertEqual(cust_updated['email'], "carlos_nuevo@mail.com")

        # 3. Eliminar
        Customer.delete_customer("C1")
        cust_deleted = Customer.display_customer_info("C1")
        self.assertIsNone(cust_deleted)

    def test_reservation_operations_positive(self):
        """Positivo: Crear y Cancelar una Reservación (Verifica inventario de habitaciones)."""
        # Configuración inicial
        Hotel.create_hotel("H1", "Resort", "Cancun", 5)
        Customer.create_customer("C1", "Ana", "ana@mail.com")

        # 1. Crear Reservación
        Reservation.create_reservation("R1", "C1", "H1")
        hotel_after_res = Hotel.display_hotel_info("H1")
        self.assertEqual(hotel_after_res['rooms'], 4, "Las habitaciones deben disminuir en 1")

        # 2. Cancelar Reservación
        Reservation.cancel_reservation("R1")
        hotel_after_cancel = Hotel.display_hotel_info("H1")
        self.assertEqual(hotel_after_cancel['rooms'], 5, "Las habitaciones deben aumentar en 1")

    # ==========================================
    # CASOS NEGATIVOS (Los 5 requeridos por rúbrica)
    # ==========================================

    def test_duplicate_hotel_creation(self):
        """Negativo: Intentar crear un hotel con un ID duplicado."""
        Hotel.create_hotel("H1", "Test Hotel", "Mexico", 10)
        Hotel.create_hotel("H1", "Duplicate Hotel", "USA", 20)
        hotels = FileManager.load_data('hotels.json')
        self.assertEqual(len(hotels), 1)

    def test_delete_non_existent_customer(self):
        """Negativo: Intentar eliminar un cliente que no existe."""
        Customer.create_customer("C1", "Juan", "juan@mail.com")
        Customer.delete_customer("C999")
        customers = FileManager.load_data('customers.json')
        self.assertEqual(len(customers), 1)

    def test_create_reservation_invalid_customer(self):
        """Negativo: Intentar reservar con un ID de cliente inexistente."""
        Hotel.create_hotel("H1", "Resort", "Cancun", 5)
        Reservation.create_reservation("R1", "C-GHOST", "H1")
        reservations = FileManager.load_data('reservations.json')
        self.assertEqual(len(reservations), 0)

    def test_create_reservation_invalid_hotel(self):
        """Negativo: Intentar reservar en un hotel inexistente."""
        Customer.create_customer("C1", "Ana", "ana@mail.com")
        Reservation.create_reservation("R1", "C1", "H-GHOST")
        reservations = FileManager.load_data('reservations.json')
        self.assertEqual(len(reservations), 0)

    def test_cancel_non_existent_reservation(self):
        """Negativo: Intentar cancelar una reservación que no existe."""
        Hotel.create_hotel("H1", "Resort", "Cancun", 5)
        Customer.create_customer("C1", "Ana", "ana@mail.com")
        Reservation.create_reservation("R1", "C1", "H1")
        Reservation.cancel_reservation("R-FAKE")
        reservations = FileManager.load_data('reservations.json')
        self.assertEqual(len(reservations), 1)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
