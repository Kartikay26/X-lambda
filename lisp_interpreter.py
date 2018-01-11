import tree_parse

# TODO: define global env here
globalEnv = {}

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
            # either spl form or application
            operator = LispStatement(self.tree[0]).evaluate()
            operands = [LispStatement(self.tree[i]).evaluate()
                        for i in range(1,len(self.tree))]
            # find operator in environment
            # if operator denotes spl form, use spl rules
        else:
            # it is either primitive data or primitive procedure
            # or it might be VARIABLE NAME denoting one of these
            x = self.tree
            if type(x) == int:
                # primitive data ... return directly
                return x
            elif type(x) == str:
                # TODO: something in the env ... try to find it
                return x
