import sqlite3
import datetime


class CarDealership:
    def __init__(self):
        self.connection = sqlite3.connect("cars.db")
        self.cursor = self.connection.cursor()

    def adding_cars(self, brand_name, car_model, year_of_production):
        self.cursor.execute('INSERT OR IGNORE INTO brands (brand_name) VALUES (?)', (brand_name,))
        self.connection.commit()
        self.cursor.execute('INSERT INTO cars(brand_name,car_model,year_of_production) VALUES(?,?,?)',
                            (brand_name, car_model, year_of_production))
        self.connection.commit()

    def list_cars(self):
        query = '''
            SELECT cars.car_id,cars.brand_name,cars.car_model,cars.year_of_production,
            COALESCE(maintenance.maintenance_date, 'No maintenance') AS last_maintenance_date
            FROM cars
            LEFT JOIN maintenance ON cars.car_id = maintenance.car_id
             '''
        self.cursor.execute(query)
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
        self.cursor.execute('DELETE FROM cars WHERE car_id = ?', (car_id,))
        self.connection.commit()

    def close(self):
        self.connection.close()


class CarDealershipUser:
    def __init__(self, dealership):
        self.dealership = dealership
        self._brand_name = None
        self._car_model = None
        self._maintenance_date = None

    @property
    def brand_name(self):
        return self._brand_name

    @brand_name.setter
    def brand_name(self, value):
        self._brand_name = value.capitalize() if value else None

    @property
    def car_model(self):
        return self._car_model

    @car_model.setter
    def car_model(self, value):
        self._car_model = value.capitalize() if value else None


    def run(self):
        while True:
            print("\n1. Add Car")
            print("2. Add Maintenance Record")
            print("3. List Cars")
            print("4. List Brands")
            print("5. Delete Car")
            print("6. Exit")

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
                print(" Goodbye...")
                break
            else:
                print("Invalid choice. Please try again.")

    def add_car(self):
        self.brand_name = input("Enter brand name: ")
        self.car_model = input("Enter car model: ")
        year_of_production = input("Enter year of production: ")
        self.dealership.adding_cars(self.brand_name, self.car_model, year_of_production)

    def list_cars(self):
        cars = self.dealership.list_cars()
        print("\nCars in the database:")
        for car in cars:
            print(car)

    def add_maintenance(self):
        car_id = input("Enter car ID: ")
        self.maintenance_date = input("Enter maintenance date (YYYY-MM-DD): ")
        cost = input("Enter maintenance cost: ")
        self.dealership.add_maintenance(car_id, self.maintenance_date, cost)

    def list_brands(self):
        print("\nBrands in the database:")
        self.dealership.list_brands()

    def delete_car(self):
        car_id = input("Enter car ID to delete: ")
        self.dealership.delete_car(car_id)
        print(f"Car with ID {car_id} deleted successfully.")

    def close(self):
        self.dealership.close()


def main():
    dealership = CarDealership()
    app = CarDealershipUser(dealership)
    app.run()
    app.close()


if __name__ == "__main__":
    main()
