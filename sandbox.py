# Example dictionary
my_dict = {
    'a': [1, 2, 3],
    'b': [4, 5],
    'c': [6, 7, 8, 9],
    'd': []
}

# Counting items in each list
total = 0
for key in my_dict:
    total += len(my_dict.get(key))

# Output the counts
print(total)