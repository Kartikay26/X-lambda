# TODO: define global env here

globalEnv = {}

class LispStatement():
    "The internal representation of a lisp statement"
    def __init__(self, tree, env=None):
        self.tree = tree
        if env is None:
            env = globalEnv
        self.environment = env
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
            # either spl form or application
            operator = self.tree[0]
            # if operator denotes spl form, use spl rules
            if operator == "def":
                assert len(self.tree) == 3
                a = self.tree[1]
                b = self.tree[2]
                self.environment[a] = LispStatement(b).evaluate()
                return self.environment[a]
            elif operator == "lambda":
                pass
            else:
                # otherwise find operator in environment
                # also check "upper" environments
                # make sure it is a function
                # evaluate arguments
                operands = [LispStatement(self.tree[i]).evaluate()
                           for i in range(1,len(self.tree))]
                # apply the function
                # (difficult!)
                pass
        else:
            # it is either primitive data or primitive procedure
            # or it might be VARIABLE NAME denoting one of these
            x = self.tree
            if type(x) == int:
                # primitive data ... return directly
                return x
            elif type(x) == str:
                return self.environment[x]
