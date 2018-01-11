import tree_parse

class LispStatement():
    "A single statement in Lisp"
    def __init__(self,statement, env=None):
        "Creates internal representation of lisp statement"
        self.statement = statement
        if env is None:
            env = LispEnvironment() # Create a global env
        self.environment = env
        self.tree = tree_parse.createTree(self.statement)
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
    def __init__(self, outer=None):
        # create a global env if called directly,
        # otherwise a sub-environment
        self.outer = outer
        if outer is None:
            self.name = "GlobalEnv"
        else:
            # do something like inheriting variables from outside
            pass
