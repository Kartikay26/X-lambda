class LispEnvironment():
    "Lisp Statement Environment holding variable/value pairs"
    def __init__(self, inherit=None):
        self.inherit = inherit
        self.env = {}
    def __setitem__(self, variable, value):
        self.env[variable] = value
    def __getitem__(self, variable):
        if variable in self.env:
            return self.env[variable]
        else:
            if self.inherit is not None:
                return self.inherit[variable]
            else:
                raise KeyError("No such variable, "+variable+".")

class LispProcedure():
    "Defines a lisp procedure given by a lambda function"
    def __init__(self, tree, outer_env):
        """Given a tree like (lambda (x) (* x x)), create an internal
         representation of the procedure"""
        self.tree = tree
        assert self.tree[0] == "lambda"
        assert len(self.tree) == 3
        assert type(self.tree[1]) == list
        # TODO: handle above cases more nicely
        self.num_args = len(self.tree[1])
        self.args = self.tree[1]
        for a in self.args:
            assert type(a) == str
        self.internal_env = LispEnvironment(outer_env)
        self.return_statement = self.tree[2]

    def apply(self, arg_values):
        """Applies the procedure to the given arguments, which are
        already evaluated. arg_values should be list of primitive
        numbers or procedures"""
        assert type(arg_values) == list
        for x in arg_values:
            assert type(x)==int or isinstance(x,LispProcedure)
        # first check whether arguments match in number
        assert len(arg_values) == self.num_args
        # then unpack arguments into environment
        for (variable,value) in zip(self.args,arg_values):
            self.internal_env[variable] = value
        # return a LispStatement with a new environment
        return LispStatement(self.return_statement,
                             self.internal_env)

class PrimitiveLispProcedure(LispProcedure):
    def __init__(self, fxn):
        self.fxn = fxn
    def apply(self, arg_values):
        return LispStatement(self.fxn(arg_values))

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
            if operator == "define":
                # TODO: refactor into another function or class
                assert len(self.tree) == 3
                a = self.tree[1]
                b = self.tree[2]
                self.environment[a] = LispStatement(b).evaluate()
                return self.environment[a]
            elif operator == "lambda":
                return LispProcedure(self.tree, self.environment)
            else:
                # otherwise find operator in environment
                if isinstance(operator, LispProcedure):
                    pass
                else:
                    operator = self.environment[operator]
                    if isinstance(operator, LispProcedure):
                        pass
                    elif type(operator) == int:
                        assert len(self.tree) == 1
                        return operator
                # also check "upper" environments
                # make sure it is a function
                # evaluate arguments
                operands = [LispStatement(self.tree[i]).evaluate()
                           for i in range(1,len(self.tree))]
                # apply the function
                new_statement = operator.apply(operands)
                return new_statement.evaluate()
        else:
            # it is either primitive data or primitive procedure
            # or it might be VARIABLE NAME denoting one of these
            x = self.tree
            if type(x) == int:
                # primitive data ... return directly
                return x
            elif type(x) == str:
                return self.environment[x]

###################################################################

# define global env

globalEnv = LispEnvironment()

globalEnv['+'] = PrimitiveLispProcedure(lambda l: sum(l))
globalEnv['-'] = PrimitiveLispProcedure(
                    lambda l: (l[0]-l[1] if len(l)==2 else -l[0])
                    )
globalEnv['*'] = PrimitiveLispProcedure(
                    lambda l: reduce(lambda x,y:x*y, l)
                    )
globalEnv['/'] = PrimitiveLispProcedure(lambda (x,y): x/y)
