import csv

def save_lla(data: dict, filename = 'unnamed_lla.csv'):
    with open(filename, mode= 'w', newline='') as file:
        writer = csv.writer(file)
        nodes = data.keys() # We are grabbing the nodes that have relevant access requests
        
        for node in nodes:
            items = data[node].items()
            row = []
            for i in items:
                row.append(i)
            writer.writerow([node] + row) 
    return

import csv

def load_lla(filename='unnamed_lla.csv'):
    data = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row:
                node = row[0]  # First element is the node name
                items = row[1:]  # The rest are key-value pairs
                data[node] = dict(zip(items[::2], items[1::2]))  # Pair keys and values
    return data
