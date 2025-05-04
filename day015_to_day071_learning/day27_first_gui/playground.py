def add(*args):
    num_sum = 0
    for n in args:
        num_sum += n
    return num_sum


# print(add(2, 5, 7, 10))

def calculate(n, **kwargs):
    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)


calculate(2, add=3, multiply=5)


class Car:

    def __init__(self, **kwargs):
        self.make = kwargs.get("make")
        self.model = kwargs.get("model")


my_car = Car(make="Nissan")
print(my_car.model)
