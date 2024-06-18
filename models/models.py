class Car:
    def __init__(self, car_id, brand_name, car_model, year_of_production, chassis_code, last_maintenance_date):
        self.car_id = car_id
        self.brand_name = brand_name
        self.car_model = car_model
        self.year_of_production = year_of_production
        self.chassis_code = chassis_code
        self.last_maintenance_date = last_maintenance_date

class Brand:
    def __init__(self, brand_name):
        self.brand_name = brand_name

class Maintenance:
    def __init__(self, maintenance_id, maintenance_date, cost, car_id):
        self.maintenance_id = maintenance_id
        self.maintenance_date = maintenance_date
        self.cost = cost
        self.car_id = car_id
