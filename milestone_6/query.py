from collections import defaultdict
from datetime import datetime

from data import personnel, stock


def get_user_name():
    username=input("Please enter the username: ")
    return username.capitalize()


def greet_user(username):
    print(f"Hello {username}, Welcome to MARIOS BROS website")
    
    

def select_operation(): 
    print("The following is the menu please choose the specific numeric associated with the choice. ")
    print("1. List items by warehouse","2. Search an item and place an order","3. Browse by category","4. Quit", sep="\n")
    print("-"*120)
    menu_selection = input("Please type the number associated with the operation: ")
    print()
    # If user selects operation 1
    if menu_selection == "1":
        item_list_by_wearhouse()
    # Else, if they pick 2
    elif menu_selection=="2":
        search_and_order_item()
        
        # Else, if they pick 3
    elif menu_selection == "3":
        browse_by_category()

    # Else, if they pick 4
    elif menu_selection == "4":
            pass

    else:
        print("*"*50)
        print("Invalid input, please enter a number between 1 and 4 for valid operation")
        print("*"*50)
   



def item_list_by_wearhouse():
    d=defaultdict(list)
    for i in stock:
        item_full_name=i["state"]+" "+i["category"]
        d[i["warehouse"]].append(item_full_name)
    for i in dict(d).keys():
        print(f"Items in warehouse {i}: \n{dict(d)[i]} \n")
        print(f"Total items in Warehouse {i} are {len(dict(d)[i])}")
        print("."*120)
    items_sum=0
    for value in dict(d).values():
        items_sum+=len(value)
    number_of_warehouse=len(dict(d).keys())
    actions.append(f"listed {items_sum} items from {number_of_warehouse} Warehouses")
    # actions.append("Hi")
    continue_session = input(f"Do you want to continue with another operation? (yes/no)")
    if continue_session == "yes":
        select_operation()

                                
def validate_user(func):
    def wrapper(*args,**kwargs):
        global username
        global user_validate            
        if user_validate:
            return func(*args,**kwargs)
        else:
            while not user_validate:
                password=input(f"\nPlease enter the password {username} to grant access to place an order: ")
                for i in personnel:   
                    if username == i['user_name'] and password == i['password']:
                        user_validate  = True
                        print("-------- Access granted to place and order -------")
                        return func(*args, **kwargs)
                    for j in i.get ('head_of', []):
                      if username == j['user_name'] and password == j['password']:
                        user_validate  = True
                        print("-------- Access granted to place and order -------")
                        return func(*args, **kwargs)
                answer = input ("User_name or password is not valid. Do you want to try again?(yes/no) : ")
                if answer =="yes":
                    user_name = get_user_name()
                elif answer == "no":
                    select_operation()    
    return wrapper




@validate_user
def placing_order(search_item,total_item_count_in_Warehouses):
    order_quantity = int(input(f"How much quantity of {search_item} do you want to order?"))
    if order_quantity <= total_item_count_in_Warehouses:
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(f"Order placed: {order_quantity} * {search_item}")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    else: 
        print("-------------------------------------------------------------------------")
        print(f"There are not this many available. The maximum quantity that can be ordered is {total_item_count_in_Warehouses}.")
        print("--------------------------------------------------------------------------")
        ask_order_max = input(f"Do you want to order the {search_item} in maximum quantity of {total_item_count_in_Warehouses}? (yes/no)")
        if ask_order_max.lower() == "yes":
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print(f"Order placed: {total_item_count_in_Warehouses} * {search_item}.")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    

def search_and_order_item():
    search_item=input("Enter the item that you are searching:").lower()
    search_item_state=" ".join(search_item.split(" ")[:-1]).capitalize()
    search_item_category= search_item.split()[-1].capitalize()
    location=[]
    item_count_in_warehouse_dict={}
    for item in stock:
        if item["state"] == search_item_state and item["category"]==search_item_category:
            date_str = item["date_of_stock"]
            date_format = '%Y-%m-%d %H:%M:%S'
            days=(datetime.now()-datetime.strptime(date_str, date_format)).days
            location.append("Warehouse"+ str(item["warehouse"])+ f" (in stock for {days} days)") 
            if item["warehouse"] in item_count_in_warehouse_dict:
                item_count_in_warehouse_dict[item["warehouse"]]+=1
            else:
                item_count_in_warehouse_dict[item["warehouse"]]=1
       
    print(f"item_count_in_warehouse_dict:{item_count_in_warehouse_dict}")
    if len(location)>0:
        print(f"\nQuantity Availability: {len(location)}\n")
        print("Location:")
        for i in location:
            print(i)
        for warehouse,count in item_count_in_warehouse_dict.items():
            if max(item_count_in_warehouse_dict.values())==count:                      
                print(f"\nMaximum availability: {count} in Warehouse {warehouse}\n")
        print("."*120)
        place_order=input(f"Do you want to place an order for the item {search_item}? (yes/no)")
        if place_order.lower()=="yes":
            placing_order(search_item,sum(item_count_in_warehouse_dict.values()))
    else:
        print("Not in stock")

    actions.append(f"Searched a {search_item}")
    continue_session = input(f"\nDo you want to continue with another operation? (yes/no)")
    if continue_session == "yes":
        select_operation()


def browse_by_category():
    # fix the code
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
    actions.append(f"Browsed the category {category_name}")
    continue_session = input(f"\nDo you want to continue with another operation? (yes/no)")
    if continue_session == "yes":
        select_operation()

actions=[]
username=get_user_name()
user_validate=False
print("*"*120)
greet_user(username)
print("."*120)
menu_selection= select_operation()
print()
print(f"Thank you for your visit, {username}")
print(f"In this session you have:")
for id, stmt in enumerate(actions):
    print(id+1,".",stmt)