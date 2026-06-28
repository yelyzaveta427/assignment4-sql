import random
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values
from faker import Faker

HOST = 'localhost'
USER = 'postgres'
PASSWORD = 'chocko777elza'
DATABASE = 'airports'
PORT = '5432'

AIRCRAFT_COUNT = 100
AIRPORT_COUNT = 50
TERMINAL_COUNT = 150
FLIGHT_COUNT = 500
SCHEDULE_COUNT = 50_000
CAFE_COUNT = 100
SHOP_COUNT = 100

PASSENGER_COUNT = 500_000
TICKET_COUNT = 500_000

CHUNK_SIZE = 50_000

fake = Faker()


def insert_aircrafts(cursor):
    print("Inserting into aircrafts...")
    query = """INSERT INTO aircrafts 
                 (aircraft_id, model) 
                 VALUES %s """

    models = ["Boeing 737", "Airbus A320", "Boeing 777", "Airbus A350", "Embraer 190"]

    aircraft_ids = []
    for i in range(1, AIRCRAFT_COUNT + 1):
        aircraft_ids.append(f"AC{i}")

    data = []
    for ac_id in aircraft_ids:
        random_model = random.choice(models)
        data.append((ac_id, random_model))

    execute_values(cursor, query, data)
    return aircraft_ids


def insert_airports(cursor):
    print("Inserting into airports...")
    query = """INSERT INTO airports 
            (airport_id, airport_name, country, city) 
            VALUES %s"""
    airport_ids = list(range(1, AIRPORT_COUNT + 1))
    data = []
    for ap_id in airport_ids:
        country = fake.country()
        city = fake.city()
        data.append((ap_id, f"{city} Airport", country, city))
    execute_values(cursor, query, data)
    return airport_ids


def insert_terminals(cursor, airport_ids):
    print("Inserting into terminals...")
    query = """INSERT INTO terminals 
            (terminal_id, airport_id, terminal_name) 
            VALUES %s"""
    terminal_ids = list(range(1, TERMINAL_COUNT + 1))
    data = []
    names = ["A", "B", "C", "D", "E"]
    for id in terminal_ids:
        data.append((id, random.choice(airport_ids), random.choice(names)))
    execute_values(cursor, query, data)
    return terminal_ids


def insert_passengers(cursor):
    print(f"Inserting into passengers...")
    query = """INSERT INTO passengers 
            (passenger_id, first_name, last_name) 
            VALUES %s"""

    passenger_ids = list(range(1, PASSENGER_COUNT + 1))

    for start in range(0, PASSENGER_COUNT, CHUNK_SIZE):
        current_chunk = min(CHUNK_SIZE, PASSENGER_COUNT - start)
        passengers_data = []

        for i in range(current_chunk):
            p_id = passenger_ids[start + i]
            f_name = fake.first_name()
            l_name = fake.last_name()
            passengers_data.append((p_id, f_name, l_name))

        execute_values(cursor, query, passengers_data)

    return passenger_ids


def insert_passports(cursor, passenger_ids):
    print(f"Inserting into passports...")
    query = """INSERT INTO passports_of_passengers 
                (passenger_id, passport_number) 
                VALUES %s"""

    for start in range(0, PASSENGER_COUNT, CHUNK_SIZE):
        current_chunk = min(CHUNK_SIZE, PASSENGER_COUNT - start)
        passports_data = []

        for i in range(current_chunk):
            p_id = passenger_ids[start + i]
            random_passport_number = str(random.randint(100000000, 999999999))

            passports_data.append((
                p_id,
                random_passport_number,
            ))

        execute_values(cursor, query, passports_data)


def insert_flights(cursor, airport_ids):
    print("Inserting into flights...")
    query = """INSERT INTO flights 
            (flight_id, departure_airport, arrival_airport) 
            VALUES %s"""
    flight_ids = list(range(1, FLIGHT_COUNT + 1))
    data = []
    for f_id in flight_ids:
        dep = random.choice(airport_ids)
        arr = random.choice(airport_ids)
        while dep == arr:
            arr = random.choice(airport_ids)
        data.append((f_id, dep, arr))
    execute_values(cursor, query, data)
    return flight_ids


def insert_schedule(cursor, flight_ids, aircraft_ids, terminal_ids):
    print(f"Inserting into schedule_of_flights...")
    query = """
        INSERT INTO schedule_of_flights 
        (schedule_id, flight_id, aircraft_id, departure_terminal_id, arrival_terminal_id, departure_date, arrival_date, status) 
        VALUES %s
    """
    schedule_ids = list(range(1, SCHEDULE_COUNT + 1))
    statuses = ["Scheduled", "On Time", "Delayed", "Departed", "Arrived", "Cancelled"]
    start_date = datetime(2024, 1, 1)
    time_step_minutes = 31

    for start in range(0, SCHEDULE_COUNT, CHUNK_SIZE):
        current_chunk = min(CHUNK_SIZE, SCHEDULE_COUNT - start)
        data = []

        for i in range(current_chunk):
            s_id = schedule_ids[start + i]
            minutes_shift = (start + i) * time_step_minutes
            dep_date = start_date + timedelta(minutes=minutes_shift)
            arr_date = dep_date + timedelta(hours=random.randint(1, 12))

            data.append((
                s_id,
                random.choice(flight_ids),
                random.choice(aircraft_ids),
                random.choice(terminal_ids),
                random.choice(terminal_ids),
                dep_date.date(),
                arr_date.date(),
                random.choice(statuses)
            ))

        execute_values(cursor, query, data)

    return schedule_ids


def insert_tickets(cursor, passenger_ids, schedule_ids):
    print(f"Inserting into tickets...")
    query = """INSERT INTO tickets 
    (ticket_id, passenger_id, schedule_id, class, price) 
    VALUES %s"""

    ticket_ids = list(range(1, TICKET_COUNT + 1))
    classes = ["Economy", "Business"]

    for start in range(0, TICKET_COUNT, CHUNK_SIZE):
        current_chunk = min(CHUNK_SIZE, TICKET_COUNT - start)
        data = []

        for i in range(current_chunk):
            t_id = ticket_ids[start + i]
            cls = random.choice(classes)

            if cls == "Business":
                price = random.randint(15000, 45000)
            else:
                price = random.randint(1200, 6800)

            data.append((
                t_id,
                random.choice(passenger_ids),
                random.choice(schedule_ids),
                cls,
                price
            ))

        execute_values(cursor, query, data)


def insert_cafes(cursor, terminal_ids):
    print("Inserting into cafes...")
    query = """INSERT INTO cafes 
    (cafe_id, name_of_cafe, food_type, terminal_id, revenue) 
    VALUES %s"""

    cafe_names = ["Starbucks", "Costa Coffee", "McDonalds", "Burger King", "SkyBar", "Bistro"]
    food_types = ["Coffee & FastFood", "FastFood", "Burgers", "Premium/Drinks", "Snacks"]

    cafe_data = [
        (i, random.choice(cafe_names), random.choice(food_types), random.choice(terminal_ids),
         random.randint(50000, 500000))
        for i in range(1, CAFE_COUNT + 1)
    ]
    execute_values(cursor, query, cafe_data)


def insert_shops(cursor, terminal_ids):
    print("Inserting into shops...")
    query = """INSERT INTO shops 
    (shop_id, name_of_shop, type_of_shop, terminal_id, revenue) 
    VALUES %s"""

    shop_names = ["Duty Free", "Relay", "News & Books", "TechStore", "Swarovski"]
    shop_types = ["Alcohol & Perfume", "Press & Tobacco", "Electronics", "Jewelry"]

    shop_data = [
        (i, random.choice(shop_names), random.choice(shop_types), random.choice(terminal_ids),
         random.randint(70000, 1000000))
        for i in range(1, SHOP_COUNT + 1)
    ]
    execute_values(cursor, query, shop_data)


def main():
    connection = psycopg2.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        dbname=DATABASE,
        port=PORT,
    )

    try:
        with connection:
            with connection.cursor() as cursor:
                aircraft_ids = insert_aircrafts(cursor)
                airport_ids = insert_airports(cursor)
                terminal_ids = insert_terminals(cursor, airport_ids)
                passenger_ids = insert_passengers(cursor)
                insert_passports(cursor, passenger_ids)
                flight_ids = insert_flights(cursor, airport_ids)
                schedule_ids = insert_schedule(cursor, flight_ids, aircraft_ids, terminal_ids)
                insert_tickets(cursor, passenger_ids, schedule_ids)
                insert_cafes(cursor, terminal_ids)
                insert_shops(cursor, terminal_ids)
    finally:
        connection.close()


if __name__ == "__main__":
    main()