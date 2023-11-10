from datetime import datetime
from loader import Loader
import colors

# -------------------------------------------------------------------  Personnel  ---------------------------------------------------------------


class User:
    def __init__(self, user_name="Anonymous") -> str:
        self._name = user_name
        self.is_authenticated = False

    def authenticate(self, password: str) -> False:
        return False

    def is_named(self, name: str) -> bool:
        if name == self._name:
            return name
        return False

    def greet(self):
        print(f"{colors.ANSI_PURPLE}{' '*30}Hello, {self._name}!\n{' '*20}Welcome to our Warehouse Database.\n{' '*16}If you don't find what you are looking for,\n{' '*14}Please ask one of our staff members to assist you.{colors.ANSI_RESET}")

    def bye(self, actions: list):
        print(
            f"{colors.ANSI_BLUE}\n{'-'*50}  Thank you for your visit, {self._name}.  {'-'*50}\n")

    def __str__(self):
        return self._name


class Employee(User):

    def __init__(self, user_name: str, password: str, head_of: list = []) -> str:
        super().__init__(user_name)
        self.__password = password
        self.head_of = head_of  # should be list of dictionaries

    def authenticate(self, password: str):
        if self.__password == password:
            return True
        print(
            f"Inside authenticate, returning False just checked- {password} : {self.__password}")
        return False

    def order(self, item: str, amount: int):
        print(f"Item Name: {item}\nQuantity ordered: {amount}")

    def greet(self):
        print(f"{colors.ANSI_GREEN}{' '*30}Hello, {self._name}!\n{' '*15}If you experience a problem with the system,\n{' '*20}Please contact technical support.{colors.ANSI_RESET}")

    def bye(self, actions: list):
        super().bye(actions)
        if len(actions) == 0:
            print(
                f"\n{colors.ANSI_RESET}{' '*20}You have not done any action in specific!")

        else:
            print(f"{colors.ANSI_RESET}\nSummary of action this session:")
            for id, stmt in enumerate(actions):
                print(" "*20, id+1, ".", stmt)


# --------------------------------------------------------------------- Stock -------------------------------------------------------------------
class Item:

    def __init__(self, state: str = None, category: str = None, date_of_stock: datetime = None, warehouse: int = None):
        self.state = state
        self.category = category
        self.date_of_stock = date_of_stock
        self.warehouse = warehouse

    def __str__(self) -> str:
        return f"{self.state} {self.category}"

    def item_list_by_wearhouse():
        stock = Loader(model="stock")
        new_item_dict = {}
        for i in stock.objects:
            if i not in new_item_dict:
                new_item_dict[i] = []
                for j in i.stock:
                    new_item_dict[i].append(str(j))

        for i in new_item_dict.keys():
            total_items_in_warehouse = [str(item) for item in new_item_dict[i]]
            print(f"{colors.ANSI_RED}Items in Warehouse {i}: {colors.ANSI_RESET}\n",
                  *total_items_in_warehouse, sep="\n")
            print(
                f"{colors.ANSI_GREEN}Total items in {i}: {len(total_items_in_warehouse)} {colors.ANSI_RESET} ")
            print(f"{'-'*100}")

        return new_item_dict


class Warehouse:

    def __init__(self, id: int = None):
        self.id = id
        self.stock = []

    def occupancy(self) -> int:
        return f"The total number of items in the stock of Warehouse {self.id}: {len(self.stock)}"

    def add_item(self, item):
        self.stock.append(item)

    def search(self, search_item) -> list:
        search_item_list = [item for item in self.stock if str(
            item)[1] == search_item.lower()]
        return search_item_list

    def __str__(self) -> str:
        return f"Warehouse {self.id}"

    def search_and_order_item(self):
        search_item = input(
            f"\n{colors.ANSI_RESET}Enter the item that you are searching: {colors.ANSI_YELLOW}").lower()
        location = []
        item_count_in_warehouse_dict = {}
        stock = Loader(model="stock")
        for warehouse in stock:
            for item in warehouse.stock:
                if search_item.lower() == str(item).lower():
                    date_str = item.date_of_stock
                    date_format = '%Y-%m-%d %H:%M:%S'
                    days = (datetime.now() -
                            datetime.strptime(date_str, date_format)).days
                    location.append(
                        f"{str(warehouse)} (in stock for {days} days)")
                    if str(warehouse) in item_count_in_warehouse_dict:
                        item_count_in_warehouse_dict[str(warehouse)] += 1
                    else:
                        item_count_in_warehouse_dict[str(warehouse)] = 1

        # print(f"item_count_in_warehouse_dict:{item_count_in_warehouse_dict}")
        return location, item_count_in_warehouse_dict, search_item

    def browse_by_category(self):
        list_item_category = []
        stock = Loader(model="stock")
        for warehouse in stock:
            for item in warehouse.stock:
                list_item_category.append(item.category)
        dict_item_category_count = {
            i: list_item_category.count(i) for i in list_item_category}
        dict_id_category = {}
        print()
        for id, (key, value) in enumerate(dict_item_category_count.items()):
            dict_id_category[id+1] = key
            print(
                f"{' '*20}{colors.ANSI_PURPLE}{id+1} {key} ({value}){colors.ANSI_RESET}")

        print()
        return dict_id_category
