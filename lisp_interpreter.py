class LispStatement():
    "A single statement in Lisp"
    def __init__(self,statement, env=globalEnv):
        "Creates internal representation of lisp statement"
        self.statement = statement
        self.environment = env
        self.tree = createTree(self.statement)
    def evaluate(self):
        "Evaluates the statement and returns its value"
        if type(self.tree) == list:
            # do something recursively?
            # creating a new environment or something?
            pass
        else:
            # it is already a primitive value
            return self.tree

class LispEnvironment():
    "Environment for lisp execution"
    def __init__(self):
        self.arg = arg
def tokeniser(string):
    "A generator that yields tokens based on input"
    NUMBER = 1
    STRING = 2
    WHITESPACE = 3
    SYMBOL = 4
    def getmode(char):
        modes = {NUMBER: '1234567890',
                 WHITESPACE: ' \t\n',
                 SYMBOL: '()'}
        for m in modes:
            if char in modes[m]:
                return m
        # else ... default mode is STRING
        return STRING

    mode = WHITESPACE
    forming_token = ""
    for ch in string:
        newmode = getmode(ch)
        if newmode == mode:
            if mode != SYMBOL:
                forming_token += ch
            else:
                yield forming_token
                forming_token = ch
        else:
            if forming_token.strip() != '':
                yield forming_token
            else:
                pass
            forming_token = ch
        mode = newmode
    yield forming_token

def createTree(string):
    "Creates a tree from a string like (+ (- 2 3) (a))"
    pass
