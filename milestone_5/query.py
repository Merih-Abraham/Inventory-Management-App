from data import stock
from datetime import datetime
# YOUR CODE STARTS HERE

# Get the user name
username=input("Please enter the username: ")

# Greet the user
print(f"Hello {username}, Welcome to the MARIOS BROS warehouse website")
# Show the menu and ask to pick a choice
print()
print("The following is the menu please choose the specific numeric associated with the choice. ")
print("1. List items by warehouse","2. Search an item and place an order","3. Browse by category","4. Quit", sep="\n")
print()
menu_selection = input("Please type the number associated with the operation: ")
    
# If they pick 1

if menu_selection == "1":
    items_in_warehouse1=[]
    items_in_warehouse2=[]
    for i in stock:
        item_full_name=i["state"]+" "+i["category"]
        if i["warehouse"]==1:
            items_in_warehouse1.append(item_full_name)
        else:
            items_in_warehouse2.append(item_full_name)

    print(f"Items in warehouse 1:")
    for id, item in enumerate(items_in_warehouse1):
        print(id+1,".",item)
    print(f"Total items in Warehouse 1 is {len(items_in_warehouse1)}")
    print()
    print("*"*100)
    print(f"Items in warehouse 2:")
    for id, item in enumerate(items_in_warehouse2):
        print(id+1,".",item)
    print(f"Total items in Warehouse 2 is {len(items_in_warehouse2)}")

# Else, if they pick 2
elif menu_selection=="2":
    search_item=input("Enter the item that you are searching:").lower()
    search_item_state=" ".join(search_item.split(" ")[:-1]).capitalize()
    print("state : ", search_item_state)
    search_item_category= search_item.split()[-1].capitalize()
    print("category:" , search_item_category)
    location=[]
    item_count_in_warehouse1=0
    item_count_in_warehouse2=0
    for item in stock:
        if item["state"] == search_item_state and item["category"]==search_item_category:
            date_str = item["date_of_stock"]
            date_format = '%Y-%m-%d %H:%M:%S'
            days=(datetime.now()-datetime.strptime(date_str, date_format)).days
            location.append("Warehouse"+ str(item["warehouse"])+ f" (in stock for {days} days)") 
            if item["warehouse"]==1:
                item_count_in_warehouse1+=1
            else:
                item_count_in_warehouse2+=1

    if len(location)>0:
        print("Quantity Availability: ", len(location))
        print("Location:")
        for i in location:
            print(i)
        if item_count_in_warehouse1>0 and item_count_in_warehouse2>0:
            if item_count_in_warehouse1>item_count_in_warehouse2:
                print(f"Maximum availability: {item_count_in_warehouse1} in Warehouse 1")
            else:
                print(f"Maximum availability: {item_count_in_warehouse2} in Warehouse 2")
        place_order=input(f"Do you want to place an order for the item {search_item}? (yes/no)")
        if place_order.lower()=="yes":
            order_quantity = int(input(f"How much quantity of {search_item} do you want to order?"))
            if order_quantity <= item_count_in_warehouse1+item_count_in_warehouse2:
                print(f"Order placed: {order_quantity} * {search_item}")
            else: 
                print("***********************************************************")
                print(f"There are not this many available. The maximum quantity that can be ordered is {item_count_in_warehouse1+item_count_in_warehouse2}.")
                print("***********************************************************")
                ask_order_max = input(f"Do you want to order the {search_item} in maximum quantity of {item_count_in_warehouse1+item_count_in_warehouse2}? (yes/no)")
                if ask_order_max.lower() == "yes":
                    print(f"Order placed: {item_count_in_warehouse1+item_count_in_warehouse2} * {search_item}.")
    else:
        print("Not in stock")
    
elif menu_selection == "3":
    list_item_category=[]
    for item in stock:
        list_item_category.append(item["category"])
    dict_item_category_count={i:list_item_category.count(i) for i in list_item_category}
    dict_id_category={}
    for id,(key,value) in enumerate(dict_item_category_count.items()):
        dict_id_category[id+1]=key
        print(f"{id+1} {key} ({value})")
    print()
    select_category=input("Type the category number to browse:")
    print(f"dict_item_category_count : {dict_item_category_count}")
    print(f"dict_id_category,{dict_id_category}")
    print()
    category_name=None
    for key_id, value_id in dict_id_category.items():
        if key_id==int(select_category):
            category_name=value_id
            count_items_by_category=0
            for item in stock:
                if value_id==item["category"]:
                    count_items_by_category+=1
                    print(f"{item['state']} {item['category']}, Warehouse {item['warehouse']}")
    print("."*120)
    print(f"Total items in this category are: {count_items_by_category}")
    print("."*120)

# Else, if they pick 3
elif menu_selection == "4":
        pass
else:
    print("******************************************************")
    print("Invalid input, please enter a number between 1 and 3 for valid operation")
    print("******************************************************")




# Thank the user for the visit
print(f"Thank you for your visit, {username.capitalize()}")