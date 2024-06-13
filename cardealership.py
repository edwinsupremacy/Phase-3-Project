import sqlite3

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
        for brand in brands:
            print(brand[0])

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

def main():
    dealership = CarDealership()
    user = CarDealershipUser(dealership)
    user.run()
    user.close()

class CarDealershipUser:
    def __init__(self, dealership):
        self.dealership = dealership
        self._brand_name = ''
        self._car_model = ''

    @property
    def brand_name(self):
        return self._brand_name

    @brand_name.setter
    def brand_name(self, value):
        self._brand_name = value.capitalize()

    @property
    def car_model(self):
        return self._car_model

    @car_model.setter
    def car_model(self, value):
        self._car_model = value.capitalize()

    def run(self):
        while True:
            print("\n1. Add Car")
            print("2. Add Maintenance Record")
            print("3. List Cars")
            print("4. List Brands")
            print("5. Delete Car")
            print("6. Search Cars ")
            print("7. Clear All Car Records")
            print("8. Exit")

            choice = input("Enter choice: ")

            if choice == '1':
                self.add_car()
            elif choice == '2':
                self.add_maintenance()
            elif choice == '3':
                self.list_cars()
            elif choice == '4':
                self.list_brands()
            elif choice == '5':
                self.delete_car()
            elif choice == '6':
                self.search_cars()
            elif choice == '7':
                self.clear_all_cars()
            elif choice == '8':
                print("ADIOS.((`-`))...")
                break
            else:
                print("Invalid choice.")

    def add_car(self):
        brand_name = input("Enter brand name: ")
        car_model = input("Enter car model: ")
        year_of_production = input("Enter year of production: ")
        chassis_code = input("Enter chassis code: ")
        self.dealership.adding_cars(brand_name, car_model, year_of_production, chassis_code)
        print('Car added successfully')

    def add_maintenance(self):
        car_id = input("Enter car ID: ")
        maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
        cost = input("Enter maintenance cost: ")
        self.dealership.add_maintenance(car_id, maintenance_date, cost)
        print('Maintenance added successfully')

    def list_cars(self):
        cars = self.dealership.list_cars()
        print("\nCars in the database:")
        for car in cars:
            print(f"{car[0]}. {car[1]} {car[2]}, Production:{car[3]}, Chassis:({car[4]}), MaintenanceDate:{car[5]}")

    def list_brands(self):
        print("\nBrands available in the database:")
        self.dealership.list_brands()

    def delete_car(self):
        car_id = input("Enter car ID to delete: ").strip()
        if not car_id.isdigit():
            print("Enter a numeric car ID.")
            return
        self.dealership.delete_car(car_id)
        print(f"Car deleted successfully.")

    def clear_all_cars(self):
        confirm = input("Are you sure you want to clear all car records? (yes/no): ")
        if confirm.lower() == 'yes':
            self.dealership.clear_all_cars()
        else:
            print("Operation cancelled.")

    def search_cars(self):
        print("\nSearch cars by:")
        print("1. Brand")
        print("2. Model")
        print("3. Year of Production")
        
        choice = input("Enter choice: ")

        if choice == '1':
            search_term = input("Enter brand name to search: ").strip()
            search_by = "brand_name"
        elif choice == '2':
            search_term = input("Enter car model to search: ").strip()
            search_by = "car_model"
        elif choice == '3':
            search_term = input("Enter year of production to search: ").strip()
            search_by = "year_of_production"
        else:
            print("Invalid choice.")
            return
        
        cars = self.dealership.search_cars(search_term, search_by)
        if cars:
            print("\nResults:")
            for car in cars:
                print(f"{car[0]}, Brand:{car[1]}, Model:{car[2]}, Production:{car[3]}, Chassis:({car[4]}), MaintenanceDate:{car[5]}")
        else:
            print("No cars found.")

    def close(self):
        self.dealership.close()

if __name__ == "__main__":
    main()
