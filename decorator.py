
class Decorator:
    def printMainMessage(func):
        def wrapper(*args):
            print("***********************************************")
            print(func(*args))
            print("***********************************************")
        return wrapper

    def mainMessage(func):
        def wrapper(*args):
            print("***********************************************")
            print("***********************************************")
            print(func(*args))
            print("***********************************************")
            print("***********************************************")
        return wrapper

    @printMainMessage
    def message(self, m):
        return m

    @mainMessage
    def mainLetter(self, m):
        return m