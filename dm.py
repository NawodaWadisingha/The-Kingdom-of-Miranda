# Importing necessary modules
import random
import datetime
import sys

# Price list dictionary containing the prices between different cities
price_list = {
    'ALVIN': {'ALVIN': 0, 'JAMZ': 20, 'ZUHAR': 20, 'RAZI': 40, 'MALI': 40},
    'JAMZ': {'JAMZ': 0, 'ALVIN': 20, 'RAZI': 20, 'MALI': 40, 'ZUHAR': 40},
    'RAZI': {'RAZI': 0, 'JAMZ': 20, 'MALI': 20, 'ALVIN': 40, 'ZUHAR': 40},
    'MALI': {'MALI': 0, 'RAZI': 20, 'ZUHAR': 20, 'ALVIN': 40, 'JAMZ': 40},
    'ZUHAR': {'ZUHAR': 0, 'ALVIN': 20, 'MALI': 20, 'JAMZ': 40, 'RAZI': 40}
}

# Vehicle prices dictionary for different vehicle types
vPrices = {
    'TRISHAW': 1,
    'CAR': 2,
    'VAN': 3}

# Promo codes dictionary with corresponding reduction values
promo = {'pro1': 1,
         'pro2': 2,
         'pro3': 3,
         'pro4': 4,
         'pro5': 5,
         'pro6': 6,
         'pro7': 7,
         'pro8': 8,
         'pro9': 9,
         'pro10': 10,
         'pro11': 11,
         'pro12': 12,
         'pro13': 13,
         'pro14': 14,
         'pro15': 15}

# Function to calculate initial price between two cities
def get_initial_price(price_list, start_place, end_place):
    return price_list[start_place][end_place]

# Function to create an invoice file for the trip
def create_invoice(start, end, final_payment, promo_reduction, random_reduction):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H_%M_%S_%f")[:24]
    time1 = current_datetime.strftime("%H:%M:%S")[:8]
    filename = f"{formatted_datetime}.txt"
    with open(filename, 'w') as file:
        file.write(f"Date:- {current_datetime.date()}\n")
        file.write(f"Time:- {time1}\n")
        file.write(f"Start:- {start}\n")
        file.write(f"End:- {end}\n")
        file.write(f"Amount:- {price_list[start][end]} KMD\n")
        file.write(f"Promo:- {promo_reduction} KMD\n")
        file.write(f"Random Reduction:- {random_reduction} KMD\n")
        file.write(f"Final payment:- {final_payment} KMD\n")

# Main function to handle user commands
def main(args):
    # Checking the minimum requirement for valid commands
    if len(args) < 2:
        print("Invalid command")
        return
    
    # Command to show the full price plan for all vehicle types
    if args[1] == "/price":
        vehicle_types = ['TRISHAW', 'CAR', 'VAN']
        for vehicle_type in vehicle_types:
            print(f"\nPrice for '{vehicle_type}':")
            for city, prices in price_list.items():
                print(f"Start {city}:")
                for destination, price in prices.items():
                    print(f"End {destination}:- {price * vPrices[vehicle_type]} KMD")
        return

    # Command to show the available commands and usage information
    if args[1] == "/?":
        print("Commands:")
        print("dm <Start> <End>:- Shows the price between the two cities and generates an invoice file for the trip")
        print()
        print("dm <Start> <End> /pro<code>:- Shows the price between the two cities after applying the promo code and generates an invoice file for the trip")
        print()
        print("dm /price:- Show the full price plan for all vehicle types in the whole country")
        print()
        print("dm <Start> <End> /<vehicle>:- Shows the price between the two cities(/c for car , /v for a van, Default is Trishaw) and generates an invoice file for the trip")
        print()
        print("dm <Start> <End> /pro<code> /<vehicle>:- Shows the price between the two cities after applying the promo code and specifies vehicle type and generates an invoice file for the trip")
        print()
        print("dm /? :- Shows the dm commands")
        return
    
    # Handling other commands with required parameters
    if len(args) < 3:
        print("Invalid command")
        return

    # Extracting the start and end places from the command-line arguments and converting them to uppercase
    start_place = args[1].upper()
    end_place = args[2].upper()

    # Initializing variables for promo code and vehicle type
    promo_code = 0
    vehicle_type = "TRISHAW"

    # Checking if the start and end places are valid cities in the price_list dictionary
    if start_place not in price_list or end_place not in price_list[start_place]:
        print("Invalid command")
        return

    # Check for promo code and vehicle type parameters
    if len(args) > 3 and not start_place == end_place:
        for arg in args[3:]:
            if arg.startswith("/pro"):
                promo_code = arg[1:]
            elif arg.startswith("/"):
                if arg[1:].upper() == 'C':
                    vehicle_type = "CAR"
                elif arg[1:].upper() == "V":
                    vehicle_type = "VAN"

    # Getting the initial price between the start and end places from the price_list dictionary
    price = get_initial_price(price_list, start_place, end_place)

    # Initializing variables for final calculations
    final_price = price
    promo_value = 0
    random_reduction = 0
    luck = 0

     # Apply promo code reduction if valid
    if promo_code in promo:
        promo_value = promo[promo_code]
        final_price = price - promo_value
    else:
        # Algorithm to generate random reduction
        if not start_place == end_place:
            luck = random.randint(0, 10)
            if luck == 1 or luck == 9:
                random_reduction = 5
                final_price = price - random_reduction

    # Apply vehicle type price multiplier and update final price
    if vehicle_type in vPrices:
        price *= vPrices[vehicle_type]
        final_price = price - promo_value - random_reduction

    # Create the invoice for the trip
    create_invoice(start_place, end_place,final_price,promo_value, random_reduction)

    # Print final details
    print(f"Amount:- {price} KMD")
    if promo_code:
        print(f"Promo Value:- {promo_value} KMD")
    if luck == 1 or luck == 9:
        print(f"Random Offer:- {random_reduction} KMD")
    print(f"Final Amount:- {final_price} KMD")

# Check if the script is being run as the main program.
if __name__ == "__main__":
    # Command-line input and calling the main function
    main(sys.argv)
