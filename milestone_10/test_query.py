from unittest.mock import Mock, MagicMock, patch
import unittest
from data import personnel, stock
from loader import Loader
import query
from classes import User, Employee, Warehouse, Item
import classes
import colors
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


class Test_query(unittest.TestCase):

    def test_user_authentication(self):
        # # test GUEST mode
        with mock_input("Mario"):
            user_name = query.get_user_name()
            with mock_input("1"):
                prints = []
                with mock_output(prints):
                    user_obj = query.user_authentication(user_name)
                self.assertTrue(isinstance(user_obj, User))
        # print(f" prints for user : {prints}")
    #     # test EMPLLOYEE mode
        with mock_input("Tom"):
            user_name = query.get_user_name()
            with patch("builtins.input", side_effect=["2", "taylor"]):
                prints_e = []
                with mock_output(prints_e):
                    user_obj = query.user_authentication(user_name)
                self.assertTrue(isinstance(user_obj, Employee))
        # print(f" prints for employee : {prints_e}")

    def test_select_operation(self):
        with mock_input("1"):
            prints = []
            with mock_output(prints):
                operation = query.select_operation()
            self.assertEqual(operation, "1")
            expected_output = ['\x1b[0m\n------------------------------------------------------------------------------------------------------------------------------------------------------', '\x1b[0mThe following is the menu please choose the specific numeric associated with the choice. ', '                         1. List items by warehouse',
                               '                         2. Search an item and place an order', '                         3. Browse by category', '                         4. Quit', '------------------------------------------------------------------------------------------------------------------------------------------------------']
            self.assertEqual(
                expected_output, prints, "The outputs are mismatching from the select operation function")

    def test_search_and_order(self):
        """Test the print_warehouse_list function."""
    
    prints = []
    actions = []  # Provide a mock for actions
    authorized_employee = "Tom"  # Provide a mock for authorized_employee

    with mock_input("Red Smartphone"):
        with mock_output(prints):
            location, item_count_in_warehouse_dict, search_item = query.search_and_order_item(actions, authorized_employee)

    if location is not None and item_count_in_warehouse_dict is not None and search_item is not None:
        # print(f" location : {location}")
        # print(f" Item count : {item_count_in_warehouse_dict}")
        # print(f"search -item : {search_item}")
        result = []
        for Warehouse in query.stock:
            search_results = Warehouse.search(search_item)
            for i in search_results:
                result.append(i)
        self.assertEqual(len(result), sum(item_count_in_warehouse_dict.values()), "The search items list is not matching")
    else:
        # Add an indented block here or fix the indentation.
        pass

def test_item_list_by_Warehouse(self):
    prints = []
    with mock_output(prints):
        new_item_dict = query.item_list_by_wearhouse()
    total_items = 0
    for i in new_item_dict.values():
        total_items += len(i)
    # print(f"total Items: {total_items}")
    # print(prints)
    self.assertEqual(total_items, 5000, "Incorrect the total items from all warehouse are 5000")
    # Add an indented block here if needed or remove the else statement.




if __name__ == "__main__":
    unittest.main()
