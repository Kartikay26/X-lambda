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

def createTree(string):
    "Creates a tree from a string like (+ (- 2 3) (a))"
    pass
