from loader import Loader
from classes import Warehouse, Item, User, Employee

# Step 3: Loading the data
personnel = Loader(model="personnel")
stock = Loader(model="stock")

# Step 4: Refactoring


def handle_user(user):
    user.greet()
    if isinstance(user, Employee):
        actions = []
        while True:
            action = input("Enter an action (order, quit): ")
            if action == "order":
                item_name = input("Enter the item name: ")
                item_amount = int(input("Enter the item amount: "))
                item = Item(state=item_name, category="example", warehouse=1, date_of_stock="2023-10-26")
                user.order(item, item_amount)
                actions.append(f"Ordered {item_amount} of {item_name}")
            elif action == "quit":
                break
        user.bye(actions)
    else:
        user.bye()


while True:
    user_name = input("Enter your name (or type 'quit' to exit): ")
    if user_name == "quit":
        break
    user = None
    for person in personnel:
        if person.is_named(user_name):
            user = person
            break
    if user is None:
        user = User(user_name)
    handle_user(user)


for warehouse in stock:
    print(f"Warehouse {warehouse.id}:")
    print(f"Occupancy: {warehouse.occupancy()}")
    search_term = input("Enter a search term: ")
    matching_items = warehouse.search(search_term)
    if matching_items:
        print("Matching Items:")
        for item in matching_items:
            print(f" - {item}")
    else:
        print("No matching items found.")
