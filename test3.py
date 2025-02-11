import csv 

test_dict = {}

test_dict[0] = {}
test_dict[1] = {}

test_dict[0][0] = False
test_dict[0][1] = False
test_dict[0][2] = False

test_dict[1][0] = False
test_dict[1][1] = True
test_dict[1][2] = True

def dict_to_csv(data: dict, filename="test.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
      
        nodes = data.keys()
        for node in nodes:
            #node is data type int
            
            values = data[node].values()
            row = []
            for v in values:
                row.append(v) 
            print(row)
            writer.writerow([node] + row)
        # Write the data rows, where each row represents a key in the dictionary
       

        
dict_to_csv(test_dict)


