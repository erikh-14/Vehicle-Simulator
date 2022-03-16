# 17 characters
# Reference: https://www.carfax.com/blog/vin-decoding
import random

class VIN:
    # possible vin digits
    vin_digits = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R','S','T','V','W','X','Y', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    
    # from 2008 to 2020
    vin_year = ['A','B','C','D','E','F','G','H','J','K','L', '8', '9']

    # possible letters
    letters = ['A','B','C','D','E','F','G','H','J','K','L','M','N','P','R','S','T','V','W','X','Y']

    # possible numbers
    numbers = ['0','1','2','3','4','5','6','7','8','9']

    # the current vin string
    vin = ''

    # World Manufacturer Identifier
    region = '1'
    company = '1'
    year = '9'

    # Dictionary of countries
    country_id = {
        'AFRICA': 'A',
        'KOREA': 'K',
        'JAPAN': 'J',
        'SWEDEN': 'S',
        'GERMANY': 'W',
        'ITALY': 'Z',
        'UNITED_STATES': '1',
        'CANADA': '2',
        'MEXICO':'3',
        'AUSTRALIA': '6'
    }

    # Dictionary of companies
    company_id = {
        'MAZDA': 'M',
        'HYUNDAI': 'H',
        'NISSAN': 'N',
        'SUBARU': 'S',
        'BMW': 'B',
        'FERRARI': 'F',
        'VOLKSWAGEN': 'V',
        'VOLVO': 'O',
        'TOYOTA':'T',
        'TESLA': 'E',
        'FORD': 'R',
        'CHEVROLET': 'C'
    }

    # Dictionary that grabs the region of a company
    company_to_region = {
        'MAZDA': country_id['JAPAN'],
        'HYUNDAI': country_id['KOREA'],
        'NISSAN': country_id['JAPAN'],
        'SUBARU': country_id['JAPAN'],
        'BMW': country_id['GERMANY'],
        'FERRARI': country_id['ITALY'],
        'VOLKSWAGEN': country_id['GERMANY'],
        'VOLVO': country_id['SWEDEN'],
        'TOYOTA': country_id['JAPAN'],
        'TESLA': '5',
        'FORD': '1',
        'CHEVROLET': '2'
    }

    def __init__ (self):
        # Generate the vin
        self.generate_vin()
#
#    def __init__ (self, region, company, year):
#        self.region = region
#        self.company = company
#        self.year = year

 #       self.generate_vin()

    # Randomly generate a VIN for testing registering vehicles
    def generate_vin(self):
        # Reset the vin
        self.vin = ""
        
        # World Manufacturer Identifier

        ## Generate company vin
        self.company = random.choice(list (self.company_id.keys()))

        ## Generate region vin
        self.region = self.company_to_region[self.company]

        ## Generate year
        self.year = random.choice(self.vin_digits)

        # Building the vin

        ## Region
        self.vin += self.region

        ## Maker
        self.vin += self.company_id[self.company]

        ## Vehicle
        self.vin += self.year


        # Vehicle Descriptor 3-8

        self.vin += random.choice(self.vin_digits)
        self.vin += random.choice(self.vin_digits)
        self.vin += random.choice(self.vin_digits)
        self.vin += random.choice(self.vin_digits)
        self.vin += random.choice(self.vin_digits)
        self.vin += random.choice(self.vin_digits)

        # Vehicle Identifier Section 9-16
        ## Year
        self.vin += random.choice(self.vin_year)

        ## Plant
        self.vin += random.choice(self.letters)

        # Sequential Numbers, can indicate assembly line sequence
        self.vin += '0'
        self.vin += random.choice(['0','1','2'])
        self.vin += random.choice(self.numbers)
        self.vin += random.choice(self.numbers)
        self.vin += random.choice(self.numbers)
        self.vin += random.choice(self.numbers)

        return self.vin

    def get_vin(self):
        return self.vin

    def get_region(self):
        return self.region

    def get_company(self):
        return self.company

    def get_year(self):
        return self.year