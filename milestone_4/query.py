from data import warehouse1, warehouse2

def list_items_by_warehouse():
    print("Items in warehouse 1:")
    for item in warehouse1:
        print(f"- {item}")

    print("\nItems in warehouse 2:")
    for item in warehouse2:
        print(f"- {item}")

def search_and_order_item(user_name):
    item_name = input("What is the name of the item? ")
    found_in_warehouse1 = item_name in warehouse1
    found_in_warehouse2 = item_name in warehouse2

    total_available = 0
    location = []

    if found_in_warehouse1:
        total_available += warehouse1.count(item_name)
        location.append("Warehouse 1")
    if found_in_warehouse2:
        total_available += warehouse2.count(item_name)
        location.append("Warehouse 2")

    if total_available == 0:
        print(f"Amount available: 0")
        print("Location: Not in stock")
    else:
        print(f"Amount available: {total_available}")
        print(f"Location: {' and '.join(location)}")

        if found_in_warehouse1 and found_in_warehouse2:
            if warehouse1.count(item_name) > warehouse2.count(item_name):
                max_available = warehouse1.count(item_name)
                max_location = "Warehouse 1"
            else:
                max_available = warehouse2.count(item_name)
                max_location = "Warehouse 2"

            print(f"Maximum availability: {max_available} in {max_location}")

        order_item = input("Would you like to order this item? (y/n) ").strip().lower()
        if order_item == 'y':
            max_available = min(total_available, max_available) if found_in_warehouse1 and found_in_warehouse2 else total_available
            quantity = int(input(f"How many would you like? "))

            if quantity <= max_available:
                print(f"{quantity} {item_name} have been ordered.")
            else:
                order_max_available = input(f"**************************************************\n"
                                            f"There are not this many available. The maximum amount that can be ordered is {max_available}\n"
                                            f"**************************************************\n"
                                            f"Would you like to order the maximum available? (y/n) ").strip().lower()
                if order_max_available == 'y':
                    print(f"{max_available} {item_name} have been ordered.")

def main():
    user_name = input("What is your user name? ")
    print(f"Hello, {user_name}!")

    while True:
        print("What would you like to do?")
        print("1. List items by warehouse")
        print("2. Search an item and place an order")
        print("3. Quit")
        choice = input("Type the number of the operation: ")

        if choice == '1':
            list_items_by_warehouse()
        elif choice == '2':
            search_and_order_item(user_name)
        elif choice == '3':
            break
        else:
            print("Unsupported operation.")

    print(f"Thank you for your visit, {user_name}!")

if __name__ == "__main__":
    main()
