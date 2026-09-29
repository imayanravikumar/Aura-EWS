# Program to demonstrate list operations
my_list = [10, 20, 30, 40, 50]
# Adding elements
my_list.append(60)
my_list.insert(2, 25)
# Removing elements
my_list.remove(40)
popped_element = my_list.pop()
# Iterating through the list
print("List elements:")
for item in my_list:
    print(item)
print(f"Popped element: {popped_element}")

# Program to demonstrate tuple operations
my_tuple = (1, 2, 3, 4, 5)
# Accessing elements
first_element = my_tuple[0]
last_element = my_tuple[-1]
# Iterating through the tuple
print("Tuple elements:")
for item in my_tuple:
    print(item)
print(f"First element: {first_element}")
print(f"Last element: {last_element}")

# Program to demonstrate dictionary operations
my_dict = {'name': 'Imayan', 'age': 25, 'city': 'Namakkal'}
# Adding key-value pairs
my_dict['email'] = 'imayan.com'
# Removing key-value pairs
del my_dict['age']
# Iterating through the dictionary
print("Dictionary elements:")
for key, value in my_dict.items():
    print(f"{key}: {value}")
