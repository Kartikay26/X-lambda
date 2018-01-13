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
            if i == "":
                continue
            if i == "DEBUG":
                # activate debug mode
                lisp_interpreter.debug = True
                continue
            while i.count("(") > i.count(")"):
                i += raw_input("... ")
        except (EOFError, KeyboardInterrupt):
            break
        if lisp_interpreter.debug:
            print "<<< ", i
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
