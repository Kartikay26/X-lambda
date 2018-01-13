from copy import deepcopy

debug = False
PrimitiveDataTypes = [int, float, bool]

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
    def __repr__(self):
        if self.inherit is None:
            return "GlobalEnv"
        else:
            return str(self.env)+"->"+str(self.inherit)

class LispProcedure():
    "Defines a lisp procedure given by a lambda function"
    def __init__(self, tree, outer_env):
        """Given a tree like (lambda (x) (* x x)), create an internal
         representation of the procedure"""
        if debug:
            print "Creating procedure,", tree, "(%s)"%(str(outer_env))
        self.tree = tree
        assert self.tree[0] == "lambda"
        assert len(self.tree) == 3
        assert type(self.tree[1]) == list
        # TODO: handle above cases more nicely
        self.num_args = len(self.tree[1])
        self.args = self.tree[1]
        for a in self.args:
            assert type(a) == str
        self.return_statement = self.tree[2]
        self.outer_env = outer_env

    def apply(self, arg_values):
        """Applies the procedure to the given arguments, which are
        already evaluated. arg_values should be list of primitive
        numbers or procedures"""
        self.internal_env = LispEnvironment(self.outer_env)
        if debug:
            print "Applying procedure,", self.tree, "(%s)"%(str(self.internal_env))
        assert type(arg_values) == list
        for x in arg_values:
            assert (type(x) in PrimitiveDataTypes or
                isinstance(x,LispProcedure))
        # first check whether arguments match in number
        assert len(arg_values) == self.num_args
        # then unpack arguments floato environment
        for (variable,value) in zip(self.args,arg_values):
            self.internal_env[variable] = value
        # return a LispStatement with a new environment
        if debug:
            print "returning from procedure",self.tree,arg_values,self.return_statement, self.internal_env
        return LispStatement(self.return_statement,
                             LispEnvironment(self.internal_env))

class PrimitiveLispProcedure(LispProcedure):
    def __init__(self, name, fxn):
        self.name = name
        self.fxn = fxn
    def apply(self, arg_values):
        if debug:
            print "calling primitive procedure",self.name,"on", arg_values
        return LispStatement(self.fxn(arg_values))

class LispStatement():
    "The internal representation of a lisp statement"
    def __init__(self, tree, env=None):
        # if debug:
        #     print "Creating statement,", tree
        #     if env is not None:
        #         print "Environment:", env
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
        if debug:
            print "Evaluating statement,", self.tree, "(%s)"%(str(self.environment))
        if type(self.tree) == list:
            # either spl form or application
            operator = self.tree[0]
            # if operator denotes spl form, use spl rules
            if operator == "define":
                # TODO: refactor floato another function or class
                assert len(self.tree) == 3
                a = self.tree[1]
                b = self.tree[2]
                globalEnv[a] = LispStatement(b).evaluate()
                return self.environment[a]
            elif operator == "lambda":
                return LispProcedure(self.tree, self.environment)
            elif operator == "if":
                if_cond = self.tree[1]
                if_true = self.tree[2]
                if_false = self.tree[3]
                if LispStatement(if_cond,
                self.environment).evaluate():
                    return LispStatement(if_true,
                            self.environment).evaluate()
                else:
                    return LispStatement(if_false,
                            self.environment).evaluate()
                pass
            else:
                # otherwise find operator in environment
                if isinstance(operator, LispProcedure):
                    pass
                else:
                    operator = self.environment[operator]
                    if isinstance(operator, LispProcedure):
                        pass
                    elif type(operator) in PrimitiveDataTypes:
                        assert len(self.tree) == 1
                        return operator
                # also check "upper" environments
                # make sure it is a function
                # evaluate arguments
                operands = [LispStatement(
                                self.tree[i],
                                self.environment
                                ).evaluate()
                                for i in range(1,len(self.tree))
                                ]
                # apply the function
                new_statement = operator.apply(operands)
                if debug:
                    print "New statement is evaluated to,",
                    print new_statement.tree
                return new_statement.evaluate()
        else:
            # it is either primitive data or primitive procedure
            # or it might be VARIABLE NAME denoting one of these
            x = self.tree
            if type(x) in PrimitiveDataTypes:
                # primitive data ... return directly
                if debug:
                    print "Statement evaluated to,",x
                return x
            elif type(x) == str:
                if debug:
                    print "Statement evaluated to,",self.environment[x]
                return self.environment[x]

###################################################################

# define global env

globalEnv = LispEnvironment()

globalEnv['+'] = PrimitiveLispProcedure('+',lambda l: sum(l))
globalEnv['-'] = PrimitiveLispProcedure('-',
                    lambda l: (l[0]-l[1] if len(l)==2 else -l[0])
                    )
globalEnv['*'] = PrimitiveLispProcedure('*',
                    lambda l: reduce(lambda x,y:x*y, l)
                    )
globalEnv['/'] = PrimitiveLispProcedure('/',lambda (x,y): float(x)/y)
globalEnv['>'] = PrimitiveLispProcedure('>',lambda (x,y): x>y)
globalEnv['<'] = PrimitiveLispProcedure('<',lambda (x,y): x<y)
globalEnv['>='] = PrimitiveLispProcedure('>=',lambda (x,y): x>=y)
globalEnv['<='] = PrimitiveLispProcedure('<=',lambda (x,y): x<=y)
globalEnv['abs'] = PrimitiveLispProcedure('abs',lambda (x,): abs(x))
