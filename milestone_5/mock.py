import os
os.makedirs('sample', exist_ok=True)
"""Mock data for this exercise."""
import json
from datetime import datetime, timedelta
from random import random, randrange

NAME_PREFIX = ('Brand new', 'Second hand', 'Almost new', 'High quality',
               'Cheap', 'Elegant', 'Funny', 'Exceptional')

NAME_MAIN = ('Monitor', 'Laptop', 'Tablet', 'Smartphone', 'Headphones',
             'Keyboard', 'Mouse', 'Router')

WAREHOUSES = ("Warehouse 1", "Warehouse 2")


def rand_integer(min_value=0, max_value=10000):
    """Return a random integer."""
    return randrange(max_value - min_value + 1) + min_value


def rand_option(options):
    """Pick an item randomly."""
    index = int(random() * len(options))
    return options[index]


def composed_name(prefix=NAME_PREFIX, suffix=NAME_MAIN):
    """Return a composed name."""
    return rand_option(prefix).capitalize() + ' ' + rand_option(suffix).lower()


def rand_date(start=None, end=None):
    """Return a random date after start."""
    if not start:
        print("the start argument is required")
        return None
    start_date = datetime.strptime(start, '%Y-%m-%d')
    if not end:
        end_date = datetime.now()
    else:
        end_date = end
    time_between_dates = end_date - start_date
    days_between_dates = int(time_between_dates.total_seconds())
    random_number_of_days = randrange(days_between_dates)
    random_date = start_date + timedelta(seconds=random_number_of_days)
    return random_date


def create(amount=100):
    """Create mock data."""
    data = []
    while len(data) < amount:
        state = rand_option(NAME_PREFIX)
        category = rand_option(NAME_MAIN)
        data.append({
            "state": state,
            "category": category,
            "warehouse": rand_integer(min_value=1, max_value=2),
            "date_of_stock": rand_date(start='2019-08-10')
            })
    return data


def save(data=None, filename="warehouse"):
    """Save the mocked data into a json file."""
    if data:
        with open(f"sample/{filename}.py", "w") as file:
            file.write("stock = ")
            file.write(json.dumps(data, default=str))


def create_and_save(amount=100, filename="warehouse"):
    """Save a mock sample as a json file."""
    data = create(amount)
    save(data, filename)


confirm = input("This will replace the data in the exercise."
                " Are you sure you want to proceed?(y/n) ")

if confirm.lower() == "y":
    create_and_save(amount=300, filename="data")
    print("The dataset has been replaced with new random mock data.")