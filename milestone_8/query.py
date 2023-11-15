from loader import Loader
from data import personnel
from datetime import datetime
from collections import defaultdict
from classes import User, Employee, Item, Warehouse
import colors

personnel=Loader(model="personnel") # list of Employees objects
stock=Loader(model="stock") # list of Warehouse objects


# for warehouse in stock:
#     # print(warehouse)
#     for i in warehouse.stock:
#         print(str(i))

# for i in personnel:
#     print(i)

# for i in personnel.objects:
#     print(i)


def get_user_name():
    username=input(f"\n{colors.ANSI_CYAN}Please enter the username: {colors.ANSI_YELLOW}")
    return username.capitalize()

def validate_user(personnel,password,user_name):
    for staff in personnel:
        if str(staff)==user_name:
            if staff.authenticate(password)==True:
                staff.is_authenticated=True
                print(f"{colors.ANSI_RESET}{'-'*150}")
                staff.greet()
                return staff

def user_authentication(user_name):
    entry_mode = input(f"\n{colors.ANSI_RESET}ENTRY MODE :\n{'*'*20} {colors.ANSI_YELLOW}1.GUEST    {colors.ANSI_RESET}{'*'*20}\n{'*'*20} {colors.ANSI_YELLOW}2.EMPLOYEE {colors.ANSI_RESET}{'*'*20}\n\nEnter the number associated with the entry mode: ")
    # guest mode
    if entry_mode=="1":
        user=User(user_name)
        print(f"{'-'*150}")
        user.greet()
        return user
    # #employee mode
    elif entry_mode=="2":
        password=input(f"Please enter your password: {colors.ANSI_YELLOW}")
        authorised_employee=validate_user(personnel,password,user_name)
        if not authorised_employee:         
            user_decision=input(f"{colors.ANSI_RED}Incorrect password for the given username.\nDo  you want to change your username and password? (y/n) : {colors.ANSI_YELLOW}")
            if user_decision=="Y" or user_decision=="y":
                start_shopping()
        return authorised_employee
    else:
        print(f"{colors.ANSI_RED} INVALID INPUT, Pleaset select the correct option.{colors.ANSI_RESET}")



def placing_order(search_item,total_item_count_in_Warehouses):
    order_quantity = int(input(f"{colors.ANSI_WHITE}\nHow much quantity of {search_item} do you want to order? {colors.ANSI_YELLOW}"))
    if order_quantity <= total_item_count_in_Warehouses:
        print(f"{colors.ANSI_RESET}{'%'*150}")
        print(f"\n{' '*50}{colors.ANSI_GREEN}Order placed: {order_quantity} * {search_item}{colors.ANSI_RESET}\n")
        print(f"{'%'*150}")
    else: 
        print(f"{colors.ANSI_RESET}{'-'*100}")
        print(f"{colors.ANSI_RED}There are not this many available. The maximum quantity that can be ordered is {total_item_count_in_Warehouses}. {colors.ANSI_RESET}")
        print("-"*100)
        ask_order_max = input(f"Do you want to order the {search_item} in maximum quantity of {total_item_count_in_Warehouses}? (y/n) -  {colors.ANSI_YELLOW} ")
        if ask_order_max.lower() in ("y","Y"):
            print(f"{colors.ANSI_RESET}{'%'*150}")
            print(f"\n{' '*50}{colors.ANSI_GREEN}Order placed: {total_item_count_in_Warehouses} * {search_item}{colors.ANSI_RESET}\n")
            print(f"{'%'*150}")



def search_and_order_item():
        search_item=input(f"\n{colors.ANSI_RESET}Enter the item that you are searching: {colors.ANSI_YELLOW}").lower()
        location=[]
        item_count_in_warehouse_dict={}
        for warehouse in stock:
            search_result=warehouse.search(search_item)
            for i in search_result:
                date_str = i[1]
                date_format = '%Y-%m-%d %H:%M:%S'
                days=(datetime.now()-datetime.strptime(date_str, date_format)).days
                location.append(f"{str(warehouse)} (in stock for {days} days)") 
                if str(warehouse) in item_count_in_warehouse_dict:
                    item_count_in_warehouse_dict[str(warehouse)]+=1
                else:
                    item_count_in_warehouse_dict[str(warehouse)]=1

        return location, item_count_in_warehouse_dict, search_item





def search_n_order(actions,authorized_employee):
    location, item_count_in_warehouse_dict, search_item = search_and_order_item()
    if len(location)>0:
        print(f"\n{colors.ANSI_RESET}Quantity Availability: {len(location)}\n")
        print("Location:")
        for i in location:
            print(f"{' ' * 15}{colors.ANSI_PURPLE}{i}{colors.ANSI_RESET}")
        for warehouse,count in item_count_in_warehouse_dict.items():
            if max(item_count_in_warehouse_dict.values())==count:                      
                print(f"\nMaximum availability: {colors.ANSI_BLUE}{count} in {warehouse}{colors.ANSI_RESET}\n")
        print("."*120)


        if isinstance(authorized_employee, Employee)==True:
            place_order=input(f"Do you want to place an order for the item {search_item}? (y/n) - {colors.ANSI_YELLOW}")
            if place_order.lower() in ("y", "Y"):
                placing_order(search_item,sum(item_count_in_warehouse_dict.values()))
    else:
        print(f"{colors.ANSI_RED}\nNot in stock")

    actions.append(f"Searched for {search_item}")
    continue_session = input(f"\n{'*' * 20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {'*' * 20}   -   {colors.ANSI_YELLOW}")
    if continue_session in ("y","Y"):
        run(actions, authorized_employee)


def category_selection(actions, authorized_employee):
    category_select=Warehouse()
    dict_id_category=category_select.browse_by_category()
    select_category=input(f"Type the category number to browse: {colors.ANSI_YELLOW}")
    print()
    category_name=None
    for key_id, value_id in dict_id_category.items():
        if key_id==int(select_category):
            category_name=value_id
            count_items_by_category=0
            for warehouse in stock:
                for item in warehouse.stock:
                    if value_id==item.category:
                        count_items_by_category+=1
                        print(f"{' ' * 25}{colors.ANSI_GREEN}{item.state} {item.category}, {warehouse}")
    if int(select_category) not in dict_id_category.keys():
        print(f"{colors.ANSI_RED}Invalid input !{colors.ANSI_RESET}")
    if not category_name==None:
        print(f"{colors.ANSI_RESET}{'.' * 120}")
        print(f"\nTotal items in this category are: {count_items_by_category}\n")
        print("."*120)
        actions.append(f"Browsed the category {category_name}")
    continue_session = input(f"\n{'*' * 20}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {'*' * 20}   -   {colors.ANSI_YELLOW}")
    if continue_session in ("y", "Y"):
        run(actions, authorized_employee)


def select_operation(): 
    print(f"{colors.ANSI_RESET}\n{'-' * 150}")
    print(f"{colors.ANSI_RESET}The following is the menu please choose the specific numeric associated with the choice. ")
    print(f"{' ' * 25}1. List items by warehouse")
    print(f"{' ' * 25}2. Search an item and place an order")
    print(f"{' ' *  25}3. Browse by category")
    print(f"{' ' *  25}4. Quit")
    print('- ' * 150)
    menu_selection = input(f"\nPlease type the number associated with the operation:  {colors.ANSI_YELLOW}")
    return menu_selection



def item_list_by_wearhouse():
        
    new_item_dict={}
    for i in stock.objects:
        if i not in new_item_dict:
            new_item_dict[i]=[]
            for j in i.stock:
                new_item_dict[i].append(str(j))

    for i in new_item_dict.keys():
        total_items_in_warehouse=[str(item) for item in new_item_dict[i]]
        print(f"{colors.ANSI_RED}Items in Warehouse {i}: {colors.ANSI_RESET}")
        for i in total_items_in_warehouse: 
            print(i)
        print(f"{colors.ANSI_GREEN}Total items in {i}: {len(total_items_in_warehouse)} {colors.ANSI_RESET} ")
        print(f"{'-'*100}")
    return new_item_dict

def run(actions, authorized_employee=None):
    menu_selection=select_operation()
    # If user selects operation 1
    if menu_selection == "1":
        new_item_dict=item_list_by_wearhouse()
        total_items=sum(len(i) for i in new_item_dict.values())
        actions.append(f"listed {total_items} items from {len(new_item_dict.keys())} Warehouses")
    # actions.append("Hi")
        continue_session = input(f"\n{{{'-'*20}}}  {colors.ANSI_PURPLE}Do you want to continue with another operation? (y/n){colors.ANSI_RESET}  {{{'-'*20}}}   -   {colors.ANSI_YELLOW}")
        if continue_session == "y" or continue_session=="Y":
            run(actions, authorized_employee)

    # Else, if they pick 2
    elif menu_selection=="2":
        search_n_order(actions,authorized_employee)
        
    #     # Else, if they pick 3
    elif menu_selection == "3":
        category_selection(actions, authorized_employee)
       
    # Else, if they pick 4
    elif menu_selection == "4":
            pass

    else:
        print("*"*150)
        print(f"{colors.ANSI_RED}Invalid input, please enter a number between 1 and 4 for valid operation{colors.ANSI_RESET}")
        print("*"*150)

                    
def start_shopping():
    actions=[]
    username=get_user_name()
    authorised_employee=user_authentication(username) # this can be either user object or employee object depending on the entry mode
    run(actions, authorised_employee)
    print()
    if isinstance(authorised_employee, User):
        authorised_employee.bye(actions)
    else:
        authorised_employee.bye(actions)
# start_shopping()