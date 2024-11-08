import random
import random
import string
import numpy as np

class doggy():
    def __init__(self, name: string):
        self.name = name
        self.max_speed = random.randint(3,10)
        self.min_speed = random.randint(1,3)
        self.test_freq = 10

    def run(self):
        return random.randint(self.min_speed, self.max_speed)
    
def generate_dog_name():
    # Generate a random 5-letter name
    name = ''.join(random.choice(string.ascii_letters).capitalize() for _ in range(5))
    return name


def generate_dog_name():
    # Generate a random 5-letter name
    name = ''.join(random.choice(string.ascii_letters).capitalize() for _ in range(5))
    return name

def race(lst):
    options = list((range(len(lst))))
    prob = []
    for dog in lst:
        prob.append(dog.test_freq)
    denom = sum(prob)
    for i in range(len(prob)):
        prob[i] = prob[i]/denom
    next_race = np.random.choice(options, size = 20, p= prob)
    
    runtime = list(range(len(lst)))
    
    for i in range(20):
        runtime[i] = lst[i].run()
    
    sorted_indices = sorted(range(len(runtime)), key=lambda i:runtime[i], reverse= True)
    best = sorted_indices[:5]    
    worst = sorted_indices[5:]

    for i in best:
        lst[i].test_freq = lst[i].test_freq + 1
    
    for i in worst:
        lst[i].test_freq = lst[i].test_freq - 1
    return 

dog_list = []
for i in range(100):
    dog = doggy(generate_dog_name())
    dog_list.append(dog)
for i in range(3):
    race(dog_list)
