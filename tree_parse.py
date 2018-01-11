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

def createTree(string, rootNode=None):
    "Creates a tree from a string like (+ (- 2 3) (a))"
    cur_node = TreeNode('') # root node
    for token in tokeniser(string):
        if token == '(':
            new_root = TreeNode('')
            cur_node.addNodeBelow(new_root)
            cur_node = new_root
        elif token == ')':
            cur_node = cur_node.above
        else:
            cur_node.addNodeBelow(TreeNode(token))
    return cur_node.below[0]

class TreeNode:
    "A single Node in a Tree"
    def __init__(self, token):
        self.token = token
        self.above = None
        self.below = []
    def addNodeBelow(self, node):
        node.above = self
        self.below.append(node)
    def toList(self):
        if len(self.below) == 0:
            try:
                return int(self.token)
            except ValueError:
                return self.token
        l = self.below
        for i in range(len(l)):
            x = l[i]
            if isinstance(x,TreeNode):
                l[i] = x.toList()
        return l
