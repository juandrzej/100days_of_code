from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

machine_on = True

while machine_on:
    order = input(f"What would you like? {menu.get_items()}: ")

    if order == "report":
        coffee_maker.report()
        money_machine.report()
    elif order == "off":
        machine_on = False
    else:
        drink = menu.find_drink(order)
        if drink is not None:
            if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)

