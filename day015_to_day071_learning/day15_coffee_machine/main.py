# menu of coffees and their ingredients
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

# resources needed for each coffee
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0,
}


def print_report():
    """Print current resources to user."""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${resources['money']}")


def check_res(drink):
    """Check if there are enough resources for a drink."""
    all_good = True

    if MENU[drink]["ingredients"]["water"] > resources["water"]:
        print("Sorry, there is not enough water.")
        all_good = False

    if MENU[drink]["ingredients"]["coffee"] > resources["coffee"]:
        print("Sorry, there is not enough coffee.")
        all_good = False

    if "milk" in MENU[drink]["ingredients"]:
        if MENU[drink]["ingredients"]["milk"] > resources["milk"]:
            print("Sorry, there is not enough milk.")
            all_good = False

    return all_good


def process_coins(drink_cost):
    """Processes coins and checks if payment was done successfully."""
    quarters = int(input("Please insert quarters: "))
    dimes = int(input("Please insert dimes: "))
    nickles = int(input("Please insert nickles: "))
    pennies = int(input("Please insert pennies: "))
    money = quarters * 0.25 + dimes * 0.10 + nickles * 0.05 + pennies * 0.01

    if money < drink_cost:
        print("Sorry that's not enough money. Money refunded.")
        return False
    elif money == drink_cost:
        return True
    else:
        print(f"Here is ${round(money-drink_cost, 2)} dollars in change.")
        return True


def remove_res(drink):
    """Removes resource after ordering coffee."""
    resources["water"] -= MENU[drink]["ingredients"]["water"]
    resources["coffee"] -= MENU[drink]["ingredients"]["coffee"]
    if "milk" in MENU[drink]["ingredients"]:
        resources["milk"] -= MENU[drink]["ingredients"]["milk"]
    resources["money"] += MENU[drink]["cost"]


# using while loop to keep making coffee until user decides to finish
machine_on = True
while machine_on:

    # choice of coffees presented to the user
    order = input("What would you like? (espresso/latte/cappuccino): ")

    # special commands
    if order == "report":
        print_report()
    elif order == "off":
        machine_on = False
    # making coffee if none of the special commands is used
    else:
        if check_res(order):
            if process_coins(MENU[order]["cost"]):
                remove_res(order)
                print(f"Here is your {order}. Enjoy!")
