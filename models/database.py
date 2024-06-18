
import sqlite3

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
        return self.cursor.fetchall()

    def search_cars(self, search_term, search_by):
        query = f'''
            SELECT cars.car_id, cars.brand_name, cars.car_model, cars.year_of_production, cars.chassis_code,
            COALESCE(maintenance.maintenance_date, 'No maintenance') AS last_maintenance_date
            FROM cars
            LEFT JOIN maintenance ON cars.car_id = maintenance.car_id
            WHERE {search_by} LIKE ?
            '''
        self.cursor.execute(query, ('%' + search_term + '%',))
        return self.cursor.fetchall()

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
        brands = self.cursor.fetchall()
        return [brand[0] for brand in brands]

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
