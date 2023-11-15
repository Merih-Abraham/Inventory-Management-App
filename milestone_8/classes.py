from datetime import datetime
from loader import Loader
import colors 

# -------------------------------------------------------------------  Personnel  ---------------------------------------------------------------
class User:
    def __init__(self,user_name="Anonymous", password=None) ->str:
        self._name=user_name
        self.is_authenticated=False

    def authenticate(self, password:str=None)->False:
        # return False
        self.is_authenticated = False
        return self.is_authenticated

    def is_named(self,name:str)->bool:
        return name==self._name
            

    def greet(self):
        print(f"{colors.ANSI_PURPLE}{' '*30}Hello, {self._name}!\n{' '*20}Welcome to our Warehouse Database.\n{' '*16}If you don't find what you are looking for,\n{' '*14}Please ask one of our staff members to assist you.{colors.ANSI_RESET}")


    def bye(self,actions:list):
        print(f"{colors.ANSI_BLUE}\n{'-'*75}  Thank you for your visit, {self._name}.  {'-'*75}{colors.ANSI_RESET}\n")

    def __str__(self):
        return self._name
    
    

class Employee(User):
    
    def __init__(self, user_name:str= None, password:str= None,**kwargs): #head_of:list=[], **kwargs):
        super().__init__(user_name, password)
        self.__password=password
        # self.head_of=head_of # should be list of dictionaries
        if "head_of" in kwargs:
            self.head_of = [Employee(**employee)
                            for employee in kwargs["head_of"]]
        else:
             self.head_of=[]

    def authenticate(self,password:str):
        if self.__password==password:
            self.is_authenticated=True
            return True
        print(f"Inside authenticate, returning False just checked- {password} : {self.__password}")
        return False

    def order(self,item:str, amount:int)->str:
        print(f"Item Name: {item}\nQuantity ordered: {amount}")

    def greet(self):
        print(f"{colors.ANSI_GREEN}{' '*30}Hello, {self._name}!\n{' '*15}If you experience a problem with the system,\n{' '*20}Please contact technical support.{colors.ANSI_RESET}")


    def bye(self,actions:list):
        super().bye(actions)
        if len(actions)==0:
            print(f"\n{colors.ANSI_RESET}{' '*20}You have not done any action in specific!")
        else:
            print(f"{colors.ANSI_RESET}\nSummary of action this session:")
            for id, stmt in enumerate(actions):
                print(" "*20,id+1,".",stmt)
        


#--------------------------------------------------------------------- Stock -------------------------------------------------------------------
class Item:

    def __init__(self, state:str=None, category:str=None, date_of_stock:datetime=None, warehouse:int=None):
        self.state = state
        self.category = category
        self.date_of_stock = date_of_stock
        self.warehouse=warehouse

    def __str__(self)->str:
        """Return a string representing the object."""
        if not self.state:
            return self.category
        return f"{self.state} {self.category}"
    
        


class Warehouse:
    # d={id:stock}

    def __init__(self, id:int=None):
        self.id=id
        self.stock=[]
       
    
    def occupancy(self)->int:
        """Return the total amount of items currently in the warehouse."""
        return len(self.stock)


    def add_item(self,item):
        self.stock.append(item)

    def search(self,search_item)->list:
        search_item_list=[]
        for item in self.stock:
            if str(item).lower()==search_item.lower():
                if isinstance(item, str):
                    search_item_list.append((str(item)))
                else:
                    search_item_list.append((str(item), item.date_of_stock))
        # search_item_list=[(str(item), item.date_of_stock) for item in self.stock if str(item).lower()==search_item.lower() if item.date_of_stock is not None else (str(item))]
        return search_item_list

    def __str__(self)->str:
        return f"Warehouse {self.id}"
    
            

    def browse_by_category(self):
        list_item_category=[]
        stock=Loader(model="stock")
        for warehouse in stock:
            for item in warehouse.stock:
                list_item_category.append(item.category)
        dict_item_category_count={i:list_item_category.count(i) for i in list_item_category}
        dict_id_category={}
        print()
        for id,(key,value) in enumerate(dict_item_category_count.items()):
            dict_id_category[id+1]=key
            print(f"{' '*20}{colors.ANSI_PURPLE}{id+1} {key} ({value}){colors.ANSI_RESET}")
        print()
        return dict_id_category
        