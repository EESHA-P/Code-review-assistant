def calculate(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        return a / b
    
def process_data(file_path):
    f = open(file_path, 'r')
    data = f.read()
    f.close()
    result = []
    for line in data.split('\n'):
        if line:
            result.append(line.strip())
    return result

class DataManager:
    def __init__(self):
        self.data = []
    
    def add(self, item):
        self.data.append(item)
    
    def get_all(self):
        return self.data

# Global variable
counter = 0

def increment():
    global counter
    counter = counter + 1
    return counter

# Main execution
if __name__ == "__main__":
    result = calculate(10, 5, '+')
    print(result)
    
    items = process_data('data.txt')
    print(items)