"""
Sistema para gestionar Hoteles, Clientes y Reservaciones.
Persiste los datos en archivos JSON en un directorio específico.
"""

import os
import json

# Definir ruta base
BASE_DIR = '/content/drive/MyDrive/PruebasSoftware2026/A6.2_ArchivosApoyo'


class FileManager:
    """Clase auxiliar para manejar operaciones de archivos."""

    @staticmethod
    def get_filepath(filename):
        """Devuelve la ruta absoluta de un archivo."""
        return os.path.join(BASE_DIR, filename)

    @staticmethod
    def load_data(filename):
        """Carga los datos de un archivo JSON."""
        filepath = FileManager.get_filepath(filename)
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            print(f"Error: No se pudo leer '{filepath}'. Devolviendo lista vacía.")
            return []

    @staticmethod
    def save_data(filename, data):
        """Guarda los datos en un archivo JSON."""
        filepath = FileManager.get_filepath(filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except IOError:
            print(f"Error: No se pudo guardar en '{filepath}'.")


class Hotel:
    """Clase para gestionar las entidades de Hotel."""
    FILE = 'hotels.json'

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms

    def to_dict(self):
        """Devuelve la representación en diccionario del hotel."""
        return self.__dict__

    @classmethod
    def create_hotel(cls, hotel_id, name, location, rooms):
        """Crea un nuevo hotel y lo guarda en el archivo."""
        hotels = FileManager.load_data(cls.FILE)
        if any(h['hotel_id'] == hotel_id for h in hotels):
            print(f"Error: El ID del hotel {hotel_id} ya existe.")
            return
        new_hotel = cls(hotel_id, name, location, rooms)
        hotels.append(new_hotel.to_dict())
        FileManager.save_data(cls.FILE, hotels)
        print(f"Hotel '{name}' creado exitosamente.")

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Elimina un hotel por su ID."""
        hotels = FileManager.load_data(cls.FILE)
        new_list = [h for h in hotels if h['hotel_id'] != hotel_id]
        if len(hotels) == len(new_list):
            print(f"Error: ID del hotel {hotel_id} no encontrado.")
        else:
            FileManager.save_data(cls.FILE, new_list)
            print(f"ID del hotel {hotel_id} eliminado.")

    @classmethod
    def display_hotel_info(cls, hotel_id):
        """Muestra la información de un hotel específico."""
        hotels = FileManager.load_data(cls.FILE)
        hotel = next((h for h in hotels if h['hotel_id'] == hotel_id), None)
        if hotel:
            print(f"Información del Hotel: {hotel}")
            return hotel
        print(f"Error: ID del hotel {hotel_id} no encontrado.")
        return None

    @classmethod
    def modify_hotel_info(cls, hotel_id, **kwargs):
        """Modifica los atributos de un hotel existente."""
        hotels = FileManager.load_data(cls.FILE)
        found = False
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                hotel.update(kwargs)
                found = True
                break

        if found:
            FileManager.save_data(cls.FILE, hotels)
            print(f"ID del hotel {hotel_id} actualizado.")
        else:
            print(f"Error: ID del hotel {hotel_id} no encontrado.")

    @classmethod
    def reserve_room(cls, hotel_id):
        """Decrementa las habitaciones disponibles de un hotel."""
        hotels = FileManager.load_data(cls.FILE)
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                if hotel['rooms'] > 0:
                    hotel['rooms'] -= 1
                    FileManager.save_data(cls.FILE, hotels)
                    return True
                print(f"Error: No hay habitaciones disponibles en el Hotel {hotel_id}.")
                return False
        print(f"Error: ID del hotel {hotel_id} no encontrado.")
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Incrementa las habitaciones disponibles de un hotel."""
        hotels = FileManager.load_data(cls.FILE)
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                hotel['rooms'] += 1
                FileManager.save_data(cls.FILE, hotels)
                return
        print(f"Error: ID del hotel {hotel_id} no encontrado.")


class Customer:
    """Clase para gestionar las entidades de Cliente."""
    FILE = 'customers.json'

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self):
        """Devuelve la representación en diccionario del cliente."""
        return self.__dict__

    @classmethod
    def create_customer(cls, customer_id, name, email):
        """Crea un nuevo cliente."""
        customers = FileManager.load_data(cls.FILE)
        if any(c['customer_id'] == customer_id for c in customers):
            print(f"Error: El ID del cliente {customer_id} ya existe.")
            return
        new_cust = cls(customer_id, name, email)
        customers.append(new_cust.to_dict())
        FileManager.save_data(cls.FILE, customers)
        print(f"Cliente '{name}' creado exitosamente.")

    @classmethod
    def delete_customer(cls, customer_id):
        """Elimina un cliente."""
        customers = FileManager.load_data(cls.FILE)
        new_list = [c for c in customers if c['customer_id'] != customer_id]
        if len(customers) == len(new_list):
            print(f"Error: ID del cliente {customer_id} no encontrado.")
        else:
            FileManager.save_data(cls.FILE, new_list)
            print(f"ID del cliente {customer_id} eliminado.")

    @classmethod
    def display_customer_info(cls, customer_id):
        """Muestra la información del cliente."""
        customers = FileManager.load_data(cls.FILE)
        cust = next(
            (c for c in customers if c['customer_id'] == customer_id),
            None
        )
        if cust:
            print(f"Información del Cliente: {cust}")
            return cust
        print(f"Error: ID del cliente {customer_id} no encontrado.")
        return None

    @classmethod
    def modify_customer_info(cls, customer_id, **kwargs):
        """Modifica la información del cliente."""
        customers = FileManager.load_data(cls.FILE)
        found = False
        for cust in customers:
            if cust['customer_id'] == customer_id:
                cust.update(kwargs)
                found = True
                break

        if found:
            FileManager.save_data(cls.FILE, customers)
            print(f"ID del cliente {customer_id} actualizado.")
        else:
            print(f"Error: ID del cliente {customer_id} no encontrado.")


class Reservation:
    """Clase para gestionar las Reservaciones."""
    FILE = 'reservations.json'

    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Devuelve la representación en diccionario de la reservación."""
        return self.__dict__

    @classmethod
    def create_reservation(cls, reservation_id, customer_id, hotel_id):
        """Crea una reservación si el hotel y el cliente existen."""
        # Verificar que el cliente existe
        cust = Customer.display_customer_info(customer_id)
        if not cust:
            print("Fallo en la reservación: Cliente no encontrado.")
            return

        # Verificar que el hotel existe y reservar habitación
        if not Hotel.reserve_room(hotel_id):
            print("Fallo en la reservación: Hotel no encontrado o sin habitaciones.")
            return

        reservations = FileManager.load_data(cls.FILE)
        new_res = cls(reservation_id, customer_id, hotel_id)
        reservations.append(new_res.to_dict())
        FileManager.save_data(cls.FILE, reservations)
        print(f"Reservación {reservation_id} creada exitosamente.")

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancela una reservación y libera la habitación."""
        reservations = FileManager.load_data(cls.FILE)
        res = next(
            (r for r in reservations if r['reservation_id'] == reservation_id),
            None
        )
        if not res:
            print(f"Error: Reservación {reservation_id} no encontrada.")
            return

        # Liberar la habitación en el hotel
        Hotel.cancel_reservation(res['hotel_id'])

        # Eliminar reservación
        new_list = [
            r for r in reservations
            if r['reservation_id'] != reservation_id
        ]
        FileManager.save_data(cls.FILE, new_list)
        print(f"Reservación {reservation_id} cancelada.")
