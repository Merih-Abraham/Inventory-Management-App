"""Command line interface to query the stock.

To iterate the source data you can use the following structure:

for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import warehouse1, warehouse2

# YOUR CODE STARTS HERE

# Get the user name
username=input("Please enter the username: ")


# Greet the user
print(f"Hello {username}, Welcome to MARIOS BROS warehouse website")



# Show the menu and ask to pick a choice

print("The following is the menu please choose the specific numeric associated with the choice. ")
print("1. List items by warehouse","2. Search an item and place an order","3. Quit", sep="\n")
menu_selection = input("Please type the number associated with the operation ")
    
# If they pick 1

if menu_selection == "1":
    print(f"Items in warehouse 1: ")
    for id,items1 in enumerate(warehouse1):
        print(id+1, ".", items1)
    print()
    print("*"*100)
    print(f"Items in warehouse 2: ")
    for id,items2 in enumerate(warehouse2):
        print(id+1, ".", items2)

# Else, if they pick 2
elif menu_selection=="2":
    search_item=input("Enter the item that you are searching.").lower()
    count_item_warehouse1 = sum(1 for item in warehouse1 if item.lower() == search_item)
    # count_item_warehouse1=warehouse1.count(search_item.lower())
    count_item_warehouse2 = sum(1 for item in warehouse2 if item.lower() == search_item)
    print("*"*100)
    total_item_quantity=count_item_warehouse1+count_item_warehouse2
    print(f"Total availability of the item considering both the warehouses are: {total_item_quantity}")
    if total_item_quantity==0:
        print("Not in stock")
    else:
        if count_item_warehouse1>0 or count_item_warehouse2>0:
            print("Both Warehouse has the stock, ", end=" ")
            if max(count_item_warehouse1,count_item_warehouse2)==count_item_warehouse1:
                print(f"Maximum quantity Location: Warehouse 1")
            else:
                print(f"Maximum quantity Location: Warehouse 2")
        else: 
            print(f"Warehouse 2 has {count_item_warehouse2}" if count_item_warehouse2>0 else f"Warehouse 1 has {count_item_warehouse1}" )


        place_order=input(f"Do you want to place an order for the item {search_item}? (yes/no)")
        if place_order.lower()=="yes":
            order_quantity = int(input(f"How much quantity of {search_item} do you want to order?"))
            if order_quantity <= total_item_quantity:
                print(f"Order placed: {order_quantity} * {search_item}")
            else: 
                print("***********************************************************")
                print(f"There are not this many available. The maximum quantity that can be ordered is {total_item_quantity}.")
                print("***********************************************************")
                ask_order_max = input(f"Do you want to order the {search_item} in maximum quantity of {total_item_quantity}? (yes/no)")
                if ask_order_max.lower() == "yes":
                    print(f"Order placed: {total_item_quantity} * {search_item}.")

# Else, if they pick 3
elif menu_selection == "3":
        pass
else:
    print("******************************************************")
    print("Invalid input, please enter a number between 1 and 3 for valid operation")
    print("******************************************************")




# Thank the user for the visit
print(f"Thank you for your visit {username}")