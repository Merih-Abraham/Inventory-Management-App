d1={"a":1,"b":2}
d2={"c":4,"a":3,"b":10000000}

user_choice=input("Enter item:")
total_item_count=0
if user_choice in d1:
    total_item_count+=d1[user_choice]

if user_choice in d2:
    total_item_count+=d2[user_choice]


print(total_item_count)
if d1[user_choice]>d2[user_choice]:
    print("Warehouse 1 has max stock with", d1[user_choice])
else:
    print("Warehouse 2 has max stock with", d2[user_choice])