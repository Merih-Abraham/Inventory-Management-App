import unittest
from data import User, Employee, Warehouse, Item
from query import (
    get_user,
    get_selected_operation,
    list_items_by_warehouse,
    search_item,
    print_warehouse_list,
    employees_only,
)
from contextlib import contextmanager

@contextmanager
def mock_input(mock):
    original_input = __builtins__.input
    __builtins__.input = lambda _: mock
    yield
    __builtins__.input = original_input

@contextmanager
def mock_output(mock):
    original_print = __builtins__.print
    __builtins__.print = lambda *value: [mock.append(val) for val in value]
    yield
    __builtins__.print = original_print

class TestClasses(unittest.TestCase):
    def test_user_creation(self):
        user = User()
        self.assertEqual(user._name, "Anonymous")
        self.assertFalse(user.is_authenticated)
        user = User("Alice")
        self.assertEqual(user._name, "Alice")
        self.assertFalse(user.is_authenticated)
        user = User("Bob", "password")
        self.assertEqual(user._name, "Bob")
        self.assertFalse(user.is_authenticated)
        user.authenticate("password")
        self.assertFalse(user.is_authenticated)

    def test_employee_creation(self):
        employee = Employee()
        self.assertEqual(employee._name, "Anonymous")
        self.assertFalse(employee.is_authenticated)
        self.assertIsNone(employee.head_of)

        employee = Employee("Alice", "password")
        self.assertEqual(employee._name, "Alice")
        self.assertTrue(employee.is_authenticated)
        self.assertEqual(employee.head_of, [])

        employee = Employee("Bob", "password", [Employee()])
        self.assertEqual(employee._name, "Bob")
        self.assertTrue(employee.is_authenticated)
        self.assertIsInstance(employee.head_of, list)

    def test_warehouse_creation(self):
        warehouse = Warehouse()
        self.assertIsNone(warehouse.id)
        self.assertEqual(warehouse.stock, [])
        self.assertEqual(warehouse.occupancy(), 0)

    def test_item_creation(self):
        item = Item("New", "Category", "2023-01-01")
        self.assertEqual(item.state, "New")
        self.assertEqual(item.category, "Category")
        self.assertEqual(item.date_of_stock, "2023-01-01")
        self.assertEqual(str(item), "New Category")

class TestQueryScript(unittest.TestCase):
    def test_get_user(self):
        employees = [Employee("Alice")]
        with mock_input("Bob"):
            user = get_user(employees)
            self.assertIsInstance(user, User)
            self.assertEqual(user._name, "Bob")

        with mock_input("Alice"):
            user = get_user(employees)
            self.assertIsInstance(user, User)
            self.assertIsInstance(user, Employee)
            self.assertEqual(user._name, "Alice")

    def test_get_selected_operation(self):
        with mock_input("1"):
            selected_operation = get_selected_operation()
            self.assertEqual(selected_operation, 1)

    def test_list_items_by_warehouse(self):
        warehouse_data = {
            1: [Item(), Item(), Item()],
            2: [Item(), Item()],
            3: [Item(), Item(), Item(), Item()],
            4: [Item(), Item()],
        }
        with mock_output([]):
            list_items_by_warehouse(warehouse_data)
            self.assertEqual(len(warehouse_data), 4)

    def test_search_item(self):
        warehouse_data = {
            1: [Item("New", "Category"), Item("Used", "Category")],
            2: [Item("New", "Other"), Item("Used", "Other")],
        }
        with mock_output([]):
            search_item(warehouse_data, "new category")
            self.assertEqual(len(warehouse_data), 2)

    def test_print_warehouse_list(self):
        warehouse_data = {
            1: [Item(), Item(), Item()],
            2: [Item(), Item()],
        }
        with mock_output([]):
            print_warehouse_list(warehouse_data)
            self.assertEqual(len(warehouse_data), 2)

    def test_employees_only_decorator(self):
        def place_an_order():
            print("Placing an order")
            return True

        decorated_function = employees_only(place_an_order)
        with mock_output([]):
            result = decorated_function(User())
            self.assertIsNone(result)
            result = decorated_function(Employee())
            self.assertTrue(result)
            self.assertEqual(result, "Placing an order")

if __name__ == "__main__":
    unittest.main()
