import sqlite3
from database.models import Car, Brand, Maintenance

def create_tables():
    connection = sqlite3.connect("cars.db")
    cursor = connection.cursor()

    cursor.execute('DROP TABLE IF EXISTS cars')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cars(
                   car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand_name TEXT NOT NULL,
                   car_model TEXT NOT NULL,
                   year_of_production TEXT NOT NULL,
                   chassis_code TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS brands(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand_name TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS maintenance(
                   maintenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   maintenance_date TEXT NOT NULL,
                   cost TEXT NOT NULL,
                   car_id INTEGER,
                   FOREIGN KEY (car_id) REFERENCES cars(car_id)
    )''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_tables()


class CarDealership:
    def __init__(self):
        self.connection = sqlite3.connect("cars.db")
        self.cursor = self.connection.cursor()

    def adding_cars(self, brand_name, car_model, year_of_production, chassis_code):
        self.cursor.execute('INSERT OR IGNORE INTO brands (brand_name) VALUES (?)', (brand_name.strip(),))
        self.connection.commit()
        self.cursor.execute('INSERT INTO cars(brand_name, car_model, year_of_production, chassis_code) VALUES(?,?,?,?)',
                            (brand_name.strip(), car_model, year_of_production, chassis_code))
        self.connection.commit()

    def list_cars(self):
        query = '''
            SELECT cars.car_id, cars.brand_name, cars.car_model, cars.year_of_production, cars.chassis_code,
            COALESCE(maintenance.maintenance_date, 'No maintenance') AS last_maintenance_date
            FROM cars
            LEFT JOIN maintenance ON cars.car_id = maintenance.car_id
            '''
        self.cursor.execute(query)
        cars = []
        for row in self.cursor.fetchall():
            car = Car(*row)
            cars.append(car)
        return cars

    def search_cars(self, search_term, search_by):
        query = f'''
            SELECT cars.car_id, cars.brand_name, cars.car_model, cars.year_of_production, cars.chassis_code,
            COALESCE(maintenance.maintenance_date, 'No maintenance') AS last_maintenance_date
            FROM cars
            LEFT JOIN maintenance ON cars.car_id = maintenance.car_id
            WHERE {search_by} LIKE ?
            '''
        self.cursor.execute(query, ('%' + search_term + '%',))
        cars = []
        for row in self.cursor.fetchall():
            car = Car(*row)
            cars.append(car)
        return cars

    def add_maintenance(self, car_id, maintenance_date, cost):
        self.cursor.execute('SELECT car_id FROM cars WHERE car_id = ?', (car_id,))
        car_exists = self.cursor.fetchone()

        if car_exists:
            self.cursor.execute('INSERT INTO maintenance (maintenance_date, cost, car_id) VALUES (?, ?, ?)',
                                (maintenance_date, cost, car_id))
            self.connection.commit()
            print(f"Maintenance record for car ID {car_id} added successfully.")
        else:
            print(f"Car ID {car_id} does not exist.")

    def list_brands(self):
        self.cursor.execute('SELECT DISTINCT brand_name FROM brands')
        brands = []
        for row in self.cursor.fetchall():
            brand = Brand(*row)
            brands.append(brand)
        return brands

    def delete_car(self, car_id):
        self.cursor.execute('SELECT brand_name FROM cars WHERE car_id=?', (car_id,))
        deleted_brand = self.cursor.fetchone()

        if deleted_brand:
            brand_name = deleted_brand[0]

            self.cursor.execute('DELETE FROM cars WHERE car_id=?', (car_id,))
            self.connection.commit()

            self.cursor.execute('SELECT COUNT(*) FROM cars WHERE brand_name = ?', (brand_name,))
            brand_count = self.cursor.fetchone()[0]

            if brand_count == 0:
                self.cursor.execute('DELETE FROM brands WHERE brand_name=?', (brand_name,))
                self.connection.commit()
            print('Car deleted successfully')
        else:
            print('Car not found')

    def clear_all_cars(self):
        self.cursor.execute('DELETE FROM maintenance')
        self.cursor.execute('DELETE FROM cars')
        self.cursor.execute('DELETE FROM brands')
        self.connection.commit()
        print("All records cleared.")

    def close(self):
        self.connection.close()

