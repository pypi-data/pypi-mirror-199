class Calculator:
    def __init__(self):
        self.memory = 0 # an initial value is 0
    
    def add(self, num): # for the addition
        self.memory += num
        return self.memory #show the current value in memory
    
    def subtract(self, num): # for the subtraction
        self.memory -= num
        return self.memory
    
    def multiply(self, num): # for the multiplication 
        self.memory *= num
        return self.memory
    
    def divide(self, num): # for the divide
        if num == 0:
            raise ValueError("Cannot divide by zero")
        self.memory /= num
        return self.memory
    
    def root(self, n): # for the root
        self.memory **= (1/n)
        return self.memory
    
    def reset(self): # to reset the memory back to 0
        self.memory = 0
        return self.memory
