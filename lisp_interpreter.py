import tree_parse

class LispEnvironment():
    "Environment for lisp execution"
    def __init__(self, outer=None):
        # create a global env if called directly,
        # otherwise a sub-environment
        self.outer = outer
        if outer is None:
            # define global environment
            self.globalEnv = True
        else:
            # do something like inheriting variables from outside
            pass

globalEnv = LispEnvironment()

class LispStatement():
    "The internal representation of a lisp statement"
    def __init__(self, statement, env=None):
        if type(statement) == list:
            self.tree = statement
        elif type(statement) == str:
            self.tree = tree_parse.createTree(statement).toList()
        else:
            raise TypeError("Provided statement should be str or list")
        if env is None:
            env = globalEnv
    def evaluate(self):
        """
        Evaluates the statement and returns its value.
        This is done according to the following steps:
        - Primitive Data elements return their own value
        - Primitive Procedures evaluate to themselves
        - Special forms are handled specially
        - To evaluate an application:
          1. Evaluate the operator
          2. Evaluate the operands
          3. Apply the procedure, by:
             a. Copying the body of the procedure;
                while substituting formal parameters
             b. Evaluating the new body
        """
        if type(self.tree) == list:
            # do something recursively?
            # creating a new environment or something?
            pass
        else:
            # it is already a primitive value
            return self.tree
