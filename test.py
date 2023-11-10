d1 = {"a": 1, "b": 2}
d2 = {"c": 4, "a": 3, "b": 10000000}

# Assuming d1 and d2 are your dictionaries
user_choice = input("Enter item: ")

# Check if the key exists in both dictionaries
if user_choice in d1 and user_choice in d2:
    if d1[user_choice] > d2[user_choice]:
        print("Condition met")
    else:
        print("Condition not met")
else:
    print(f"The item '{user_choice}' is not present in either dictionary.")
