import csv 

test_dict = {}

test_dict[0] = {}
test_dict[1] = {}
test_dict[0][0] = False
test_dict[0][1] = False
test_dict[0][2] = False

test_dict[1][0] = True
test_dict[1][1] = True
test_dict[1][2] = True

def dict_to_csv(data: dict, filename="lla.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        nodes = data.keys()
        
        for node in nodes:
            #node is data type int
            
            values = data[node].values()
            row = []
            for v in values:
                row.append(v) 
            writer.writerow([node] + row)
    return        
        # Write the data rows, where each row represents a key in the dictionary
       
def csv_to_dict(filename: str) -> dict:
    
    with open(filename, mode='r') as f:
        reader = csv.reader(f)
        # Each row is stored as a list inside list "data"
        data = [row for row in reader]

        #creating an empty dictionary
        lla_dict = {}
        
        # iterate through each list containing bool values
        for i, row_data in enumerate(data):
            
            # Creating an empty dictionary for each node
            node_dict = {}
            # skip the first value (node int value), and add the index and bool value into the dictionary
      
            for j, d in enumerate(row_data[1:]):
                
                # This part is rediculous, if you wrap any string with bool, it will become True if the string isn't empty
               
                if d == 'True':
                    node_dict[j] = True
                else:
                    node_dict[j] = False
            lla_dict[i] = node_dict    
            
   
    return lla_dict


