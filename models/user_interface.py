from database.models import Car, Brand, Maintenance

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
            print("6. Search Cars")
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
                print("Goodbye!")
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
            print(f"{car.car_id}. {car.brand_name} {car.car_model}, Production:{car.year_of_production}, Chassis:({car.chassis_code}), MaintenanceDate:{car.last_maintenance_date}")

    def list_brands(self):
        print("\nBrands available in the database:")
        brands = self.dealership.list_brands()
        for brand in brands:
            print(brand.brand_name)

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
                print(f"{car.car_id}, Brand:{car.brand_name}, Model:{car.car_model}, Production:{car.year_of_production}, Chassis:({car.chassis_code}), MaintenanceDate:{car.last_maintenance_date}")
        else:
            print("No cars found.")

    def close(self):
        self.dealership.close()
