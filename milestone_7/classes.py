class Warehouse:
    def __init__(self, warehouse_id):
        self.id = warehouse_id
        self.stock = []

    def occupancy(self):
        return len(self.stock)

    def add_item(self, item):
        self.stock.append(item)

    def search(self, search_term):
        return [item for item in self.stock if search_term in item.state]

class Item:
    def __init__(self, state, category, warehouse, date_of_stock):
        self.state = state
        self.category = category
        self.warehouse = warehouse
        self.date_of_stock = date_of_stock

    def __str__(self):
        return f"Item: {self.state}, Category: {self.category}"

class User:
    def __init__(self, user_name):
        self._name = user_name
        self.is_authenticated = False

    def authenticate(self, password):
        return False

    def is_named(self, name):
        return self._name == name

    def greet(self):
        print(f"Hello, {self._name}!")
        print("Welcome to our Warehouse Database.")
        print("If you don't find what you are looking for, please ask one of our staff members to assist you.")

    def bye(self, actions=None):
        if actions:
            print("Actions during the session:")
            for action in actions:
                print(f"- {action}")
        print(f"Thank you for your visit, {self._name}!")

class Employee(User):
    def __init__(self, user_name, password, head_of=None):
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of if head_of else []

    def authenticate(self, password):
        return self.__password == password

    def order(self, item, amount):
        print(f"Ordered {amount} of {item.state}")

    def greet(self):
        super().greet()
        print("If you experience a problem with the system, please contact technical support.")
