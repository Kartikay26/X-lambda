import main
import lisp_interpreter
import tree_parse
import unittest

class TestProcedures(unittest.TestCase):
    "Test functioning of LispProcedure class"
    def testSimpleProcedure(self):
        p = lisp_interpreter.LispProcedure(['lambda',['x'],['x']],{})
        r = p.apply([2]).evaluate()
        e = 2
        self.assertEqual(e, r)
    def testArithmeticProcedure(self):
        p = lisp_interpreter.LispProcedure(['lambda',['x'],['*','x','x']],{})
        r = p.apply([2]).evaluate()
        e = 4
        self.assertEqual(e, r)

class TestTokeniser(unittest.TestCase):
    "Test the functioning of the tokeniser"
    def testComplexExpression(self):
        t = list(tree_parse.tokeniser("(+ (- 2 3) (a))"))
        x = ['(','+','(','-','2','3',')','(','a',')',')']
        self.assertEqual(x, t)
    def testSimpleExpression(self):
        t = list(tree_parse.tokeniser("(- 2 3)"))
        x = ['(','-','2','3',')']
        self.assertEqual(x, t)
    def testIntLiteral(self):
        t = list(tree_parse.tokeniser("2"))
        x = ['2']
        self.assertEqual(x, t)

class TestCreateTree(unittest.TestCase):
    "Test the function createTree in tree_parse"
    def testComplexExpression(self):
        t = tree_parse.createTree("(+ (- 2 3) (a))").toList()
        self.assertEqual(['+',['-',2,3],['a']], t)
    def testSimpleExpression(self):
        t = tree_parse.createTree("(- 2 3)").toList()
        self.assertEqual(['-',2,3], t)
    def testIntLiteral(self):
        t = tree_parse.createTree("2").toList()
        self.assertEqual(2, t)

unittest.main()
