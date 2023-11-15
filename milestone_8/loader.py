"""Data loader."""

from data import personnel as employees
from data import stock as items # list of dict(items)
# from classes import User,Employee,Warehouse, Item


class MissingClassError(Exception):
    """Missing class exception."""

    def __init__(self, name=None, message="Missing class."):
        """Constructor."""
        if name:
            self.class_name = name
            self.message = f"Missing class {name}."
        super().__init__(self.message)


class MissingArgument(Exception):
    pass


class Loader:
    """Main data loader class."""

    model = None
    objects = None

    def __init__(self, *args, **kwargs):
        """Constructor."""
        if "model" not in kwargs:
            raise MissingArgument("The loader requires a `model` keyword argument to work.")
        self.model = kwargs["model"]
        self.parse()

    def parse(self):
        """Instantiate objects from the data."""
        if self.model == "personnel":
            self.objects = self.__parse_personnel() # list of employee objects
        if self.model == "stock":
            self.objects = self.__parse_stock()

    def __load_class(self, name):
        """Return a class."""
        classes = __import__("classes")
        if not hasattr(classes, name):
            raise MissingClassError(name)
        return getattr(classes, name)

    def __parse_personnel(self):
        """Parse the personnel list."""
        Employee = self.__load_class("Employee")
        # print(f"Employee:{Employee}, {type(Employee)}")

        return [Employee(**employee) for employee in employees]

    def __parse_stock(self):
        """Parse the stock."""
        Item = self.__load_class("Item")
        Warehouse = self.__load_class("Warehouse")
        warehouses = {}
        for item in items:
            warehouse_id = str(item["warehouse"])
            if warehouse_id not in warehouses.keys():
                warehouses[warehouse_id] = Warehouse(warehouse_id)
            warehouses[warehouse_id].add_item(Item(**item))
        # print(warehouses.keys())
        # print(warehouses.values())
        return list(warehouses.values())

    def __iter__(self, *args, **kwargs):
        """Iterate through the objects."""
        yield from self.objects



# personnel=Loader(model="personnel") # list of Employees objects
# # stock=Loader(model="stock") # list of Warehouse objects