from unittest.mock import Mock, MagicMock, patch
import unittest
from data import personnel, stock
from loader import Loader
import query
from classes import User,Employee, Warehouse , Item
import classes
import colors


class Test_classes(unittest.TestCase):

    def test_class_name(self):
        classes=__import__("classes")
        u1 = True if hasattr(classes, "User") else False
        e1 = True if hasattr(classes, "Employee") else False
        w1 = True if hasattr(classes, "Warehouse") else False
        i1 = True if hasattr(classes, "Item") else False
        self.assertTrue(u1)
        self.assertTrue(e1)
        self.assertTrue(w1)
        self.assertTrue(i1)
    
    def test_for_inheritence(self):
        self.assertTrue(issubclass(Employee,User))

    def test_User(self):
        u1=User() # user without name
        self.assertEqual(u1._name, "Anonymous", "Incorrect output the user should be Anumymous as we have not provided the name")
        u1.authenticate("Anonymous")
        self.assertEqual(u1.is_authenticated, False, "Authentication should be False")
        # User with name
        u2=User("Sharanya")
        self.assertEqual(u2._name, "Sharanya", "Incorrect output the user name should be Sharanya")
        u2.authenticate("Sharanya")
        self.assertEqual(u2.is_authenticated, False, "Authentication should be False")
        # user with name and pwd
        u3=User("Sharanya", "7777777")
        self.assertEqual(u3._name, "Sharanya", "Incorrect output the user name should be Sharanya with psw=7777777")
        u3.authenticate("7777777")
        self.assertEqual(u3.is_authenticated, False, "Authentication should be False")
    

    def test_Item(self):
        i1=Item(state= "Red", category= "Mouse", warehouse= 2, date_of_stock="2021-05-26 17:20:10")
        self.assertEqual([i1.state,i1.category,i1.date_of_stock],["Red","Mouse","2021-05-26 17:20:10"], "The properties of the Item objects are not stored properly")
        self.assertEqual(str(i1),i1.state+" "+i1.category)


    def test_Employee(self):
        e1=Employee() # With out name, pwd
        self.assertEqual(e1.is_authenticated,False,"e1.is_authenticated should be false for employee with no name and pwd")
        self.assertEqual(e1.head_of,[],"e1.head_of should be empty for unknown employee")
        # Employee with name, pwd and set is_authenticated to True
        e2=Employee(user_name="DCI", password="zzzz", head_of=[])
        e2.authenticate("zzzz")
        self.assertTrue(e2.is_authenticated,"e2.is_authenticted is True for pwd=zzzz")
        self.assertEqual(e1.head_of,[],"e1.head_of not set")
        # Employee with name, pwd, head_of
        e3=Employee(user_name="DCI", password="zzzz", head_of=[{"user_name": "Test2", "password": "4321","head_of":[]}])
        e3.authenticate("zzzz")
        self.assertTrue(e3.is_authenticated)
        self.assertFalse(e3.head_of is [])
        self.assertTrue(isinstance(e3.head_of, list))
        for other in e3.head_of:
        #     print(f"other : {other}")
            self.assertTrue(isinstance(other, Employee))

    def test_Warehouse(self):
        w1=Warehouse()# Warehouse obj without parameter
        self.assertEqual(w1.id,None, "Incorrect Warehouse obj without parameter sets id to None")
        # Warehouse obj with id 1) to check stock property 2)chec for occupancy method
        w2=Warehouse(1) 
        self.assertEqual(w2.id,1, "Incorrect Warehouse obj with parameter 1 sets id to 1")
        self.assertEqual(w2.stock,[], "Incorrect the list property is default and set to []")
        self.assertEqual(type(w2.stock),list, "Incorrect the list property is default and set to list")
        stock_len=len(w2.stock)
        self.assertEqual(w2.occupancy(),stock_len, "Incorrect the method occupancy should return empty stock list")
        i1=Item(state= "Blue", category= "Mouse", warehouse= 2, date_of_stock="2021-05-26 17:20:10")
        i2=Item(state= "Red", category= "Mouse", warehouse= 1, date_of_stock="2021-05-26 17:20:10")
        i3=Item(state= "Orange", category= "Mouse", warehouse= 2, date_of_stock="2021-05-26 17:20:10")
        i4=Item(state= "Green", category= "Mouse", warehouse= 1, date_of_stock="2021-05-26 17:20:10")
        w2.add_item(i1)
        w2.add_item(i2)
        self.assertEqual(w2.occupancy(),stock_len+2, "Incorrect the method occupancy should return the len of stock list")
        # testing search method
        w2.add_item(i2)
        w2.add_item(i3)
        w2.add_item(i4)
        w2.add_item(i2)
        self.assertEqual( [('Red Mouse', '2021-05-26 17:20:10'), ('Red Mouse', '2021-05-26 17:20:10'), ('Red Mouse', '2021-05-26 17:20:10')], w2.search("Red Mouse"), "Incorrect there are 3 quantuty of Red Mouse in the stock")
        self.assertEqual( [('Red Mouse', '2021-05-26 17:20:10'), ('Red Mouse', '2021-05-26 17:20:10'), ('Red Mouse', '2021-05-26 17:20:10')], w2.search("rED mOUse"), "Incorrect there are 3 quantuty of item2 in the stock")



if __name__=="__main__":
    unittest.main()