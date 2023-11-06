"""Command line interface to query the stock.
To iterate the source data you can use the following structure:
for item in warehouse1:
    # Your instructions here.
    # The `item` name will contain each of the strings (item names) in the list.
"""

from data import stock, personnel
from datetime import datetime as dt
from collections import Counter

def get_user_name():
    name = input("Please provide your name: ")
    return name

def greet_user():
    print("Hello",user_name)

def display_menu(menu):
    print ("Menu")
    for k, v in menu.items(): 
        print (f"{k}: {v}")

def get_selected_operation():
    selected_operation = input("Make your choice: ")
    return selected_operation

def count_of_warehouse():
    list_of_warehouse = list({item["warehouse"] for item in stock})
    return list_of_warehouse

def list_items_by_warehouse():

    count_of_warehouse = list({item["warehouse"] for item in stock})
    count_of_items ={}

    for i in range(1,(len(count_of_warehouse)+1)):
        temp = 0
        print(f"\nItems in Warehouse{count_of_warehouse[i-1]}\n")
        for item in stock:
            if item["warehouse"] == i:
                print(f"{item['state']} {item['category']}")
                temp += 1
                count_of_items[i] = temp             

    print("\n")

    for k, v in count_of_items.items():
        print(f"Total items in warehouse {k}: {v}")

    return f"Listed {len(stock)} items."



def get_item(input_item):
    lst_item = input_item.split(" ")

    if len(lst_item) == 3:
        category = " ".join([lst_item[0], lst_item[1]])
        state = lst_item[2]

    elif len (lst_item) ==2:
        category = lst_item[0]
        state = lst_item[1]
    else:
        raise ValueError("Input is not valid. Try again")

    return category.lower(), state.lower()

def search_and_order_item():

    try:

        item_input = input("What is the name of the item? ")
        selected_item =" ".join(get_item(item_input))
        state, category = get_item(selected_item)

        list_of_warehouse = count_of_warehouse()

        info_of_item = []
        count = {}

        today = dt.now().date()
        for i in range(1, (len(list_of_warehouse)+1)):
            temp = 0
            for item in stock:
                if item['state'].lower() == state and item['category'].lower() ==category and item['warehouse'] == i:
                    date_of_stock = dt.strptime(item["date_of_stock"].split()[0],'%Y-%m-%d').date()
                    days_in_stock = (today - date_of_stock).days 
                    info_of_item.append({f"- Warehouse {i}" : f"(in stock for {days_in_stock} days)"})
                    temp += 1
                    count[f'Warehouse {i}'] = temp


        total = len(info_of_item)

        print(f"Amount available: {total}")

        print("Location:")

        if total > 0:

            for item in info_of_item:
                for k,v in item.items():
                    print(k, v)

            maximum_in_warehouse = [(k, v) for k,v in count.items() if v == max(v for v in count.values())]

            max_wrh, max_item = maximum_in_warehouse[0]

            print (f"\nMaximum availability: {max_item} in {max_wrh}")

            order = input("Would you like to order this item?(y/n): ").lower()
            if order== "n":
                return 

            elif order == "y":

                return order_item(selected_item, total)

            else:
                print( "Your answer has to be y or n")

        else:
            print("Not in stock")

        return f"Search a {selected_item.capitalize()}"

    except ValueError:
        print('Input is not valid. Item includes more words then one.')
        search_and_order_item()

def check_user_validation(func):

    def wrapper(*args, **kwargs):
        global user_name
        global user_validation
        if user_validation:
            return func(*args, **kwargs)
        else:
            while not user_validation:
                password = input("Please input your password: ")
                for i in personnel:
                    if user_name == i['user_name'] and password == i['password']:
                        user_validation  = True
                        return func(*args, **kwargs)
                    for j in i.get ('head_of', []):
                      if user_name == j['user_name'] and password == j['password']:
                        user_validation  = True
                        return func(*args, **kwargs)

                answer = input ("User_name or password is not valid. Do you want to try again?y/n")
                if answer =="y":
                    user_name = get_user_name()
                elif answer == "n":
                    session_operation()

    return wrapper

@check_user_validation
def order_item(selected_item, total):
    while True:
            quantity = int(input("How many would you like? "))
            if quantity > total:
                print(f"There are not this many available. The maximum amount that can be ordered is {total}")
            elif quantity <= total:
                print( f"{quantity} {selected_item.capitalize()} have been placed")
                break
    return f"Search and ordered the {selected_item.capitalize()}"  

def browse_by_category():

    categories = []
    for item in stock:
        categories.append(item["category"])

    count = Counter(categories)

    summary_of_categories = []

    i = 1
    for k, v in count.items():
        summary_of_categories.append((i, k, v))
        i+=1

    for i in summary_of_categories:
        print(f"{i[0]}. {i[1]} ({i[2]})")


    number_of_category = int(input("Type the number of the category to browse: "))

    selected_category = None

    for category_info in summary_of_categories:
        if number_of_category == category_info[0]:
            selected_category = category_info[1]
            break  

    print(f"\nList of {selected_category} available:")

    for i in stock:
        if i['category'] == selected_category:
            match_state = i["state"]
            match_warehouse = i["warehouse"]
            print(f"{match_state} {selected_category.lower()}, Warehouse {match_warehouse}")
        else: 
            ("Input is not valid")
            session_operation()

    return f"Browsed the category {selected_category}"                     

session_actions = []

def session_operation():

    menu = {"1": "List items by warehouse", "2": "Search an item and place an order","3": "Browse by category", "4": "Quit" }
    display_menu(menu)
    operation = get_selected_operation()

    if operation == 4:
        pass

    elif operation != 4 :
        if operation == "1":
                action = list_items_by_warehouse()
                session_actions.append(action)        
        elif operation == "2":
                action = search_and_order_item()
                session_actions.append(action)         
        elif operation == "3":
            action = browse_by_category()
            session_actions.append(action)

        else:
            print("*" * 50)
            print(operation, "is not a valid operation.")
            print("*" * 50)
            session_operation()

        working_continue = input("Would you like to continue to work with program?(y/n) ").lower()

        if working_continue == "y":
            session_operation()
        elif working_continue != "n":
            print ("Your answer has to be y or n")

user_name = get_user_name()
greet_user()
user_validation = False
session_operation()
print(f"Thank you for your visit, {user_name}!")

if session_actions:
        print("In this session you have:")
        for i, action in enumerate(session_actions, start=1):
            print(f"""    {i}. {action}""")


