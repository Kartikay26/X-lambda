"""
Trying to make a lisp interpreter in python
"""

import lisp_interpreter

def main():
    "Starts the main REPL loop"
    print "Hello!"
    while True:
        # read
        try:
            i = raw_input(">>> ")
        except (EOFError, KeyboardInterrupt):
            break
        l = lisp_interpreter.LispStatement(i)
        # eval
        r = l.evaluate()
        # print
        print r
        # loop ... (while)
    print "\nBye!"

if __name__=="__main__":
    main()
