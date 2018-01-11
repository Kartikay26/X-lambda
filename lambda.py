"""
Trying to make a lisp interpreter in python
"""

class LispStatement():
    "A single statement in Lisp"
    def __init__(self,statement):
        pass
    def evaluate(self):
        return 0

def main():
    "Starts the main REPL loop"
    print "Hello!"
    while True:
        # read
        try:
            i = raw_input(">>> ")
        except EOFError:
            break
        l = LispStatement(i)
        # eval
        r = l.evaluate()
        # print
        print r
        # loop ... back to 12
    print "Bye!"

if __name__=="__main__":
    main()
