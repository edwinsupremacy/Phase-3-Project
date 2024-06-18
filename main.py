from models import CarDealership
from user import CarDealershipUser

def main():
    dealership = CarDealership()
    user = CarDealershipUser(dealership)
    user.run()
    user.close()

if __name__ == "__main__":
    main()
