class T_node:
    def __init__(self, value, depth):
        self.value = value
        self.next = {}
        self.depth = depth
        print('created node with value: ', value)
    
    def create_children(self, values, depth):
        if self.depth == depth:
            return
        for value in values:
            self.next.append(T_node(value, depth))

