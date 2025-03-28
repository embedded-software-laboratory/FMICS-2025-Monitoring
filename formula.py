class Formula(object):
    def __eq__(self, value):
        return str(self) == str(value)

    def __hash__(self):
        return hash(str(self))

class Operator(Formula):
    def __init__(self, children):
        self.children = children

class BinaryOperator(Operator):
    def __init__(self, left, right):
        Operator.__init__(self, [left, right])
    
    def __str__(self):
        return "({} {} {})".format(self.children[0], self.operator, self.children[1])

class UnaryOperator(Operator):
    def __init__(self, child):
        Operator.__init__(self, [child])
    
    def __str__(self):
        return "{}({})".format(self.operator, self.children[0])

class Not(UnaryOperator):
    operator = u"!"

    def __init__(self, child):
        UnaryOperator.__init__(self, child)

class And(BinaryOperator):
    operator = u"^"

    def __init__(self, left, right):
        BinaryOperator.__init__(self, left, right)

class Or(BinaryOperator):
    operator = u"V"

    def __init__(self, left, right):
        BinaryOperator.__init__(self, left, right)

class G(UnaryOperator):
    operator = "G"

    def __init__(self, child):
        UnaryOperator.__init__(self, child)

class F(UnaryOperator):
    operator = "F"

    def __init__(self, child):
        UnaryOperator.__init__(self, child)

class X(UnaryOperator):
    operator = "X"

    def __init__(self, child):
        UnaryOperator.__init__(self, child)

class W(UnaryOperator):
    operator = "W"

    def __init__(self, child):
        UnaryOperator.__init__(self, child)

class U(BinaryOperator):
    operator = "U"

    def __init__(self, left, right):
        BinaryOperator.__init__(self, left, right)

class AP(Formula):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return self.name

# Syntactic sugar
def Implies(left, right):
    return Or(Not(left), right)
