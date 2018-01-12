"""
Trying to make a lisp interpreter in python
"""

import tree_parse
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
        # eval
        t = tree_parse.createTree(i).toList()
        l = lisp_interpreter.LispStatement(t)
        r = l.evaluate()
        # print
        print r
        # loop ... (while)
    print "\nBye!"

if __name__=="__main__":
    main()
