class Stack:

    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if not self.is_empty():
            return self.elements.pop()
        else:
            raise IndexError

    def peek(self):
        if not self.is_empty():
            return self.elements[-1]
        else:
            raise IndexError

    def size(self):
        return len(self.elements)


def check_balance(data):
    stack = Stack()
    opening = '([{'
    closing = ')]}'
    pairs = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    for item in data:
        if item in opening:
            stack.push(item)
        elif item in closing:
            print(pairs[item])
            if stack.is_empty() or stack.pop() != pairs[item]:
                return 'Несбалансированно'
    return 'Сбалансированно' if stack.is_empty() else 'Несбалансированно'



if __name__ == '__main__':
    input_ = input('Строка со скобками: ')
    result = check_balance(input_)
    print(result)