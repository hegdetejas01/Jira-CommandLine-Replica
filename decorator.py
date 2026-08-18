
class Decorator:
    def printMainMessage(func):
        def wrapper(*args):
            print("************************")
            print(func(*args))
            print("************************")
        return wrapper

    @printMainMessage
    def message(self, m):
        return m