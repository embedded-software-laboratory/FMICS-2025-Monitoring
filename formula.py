class Formula:
    def __eq__(self, value):
        return str(self) == str(value)

class Operator(Formula):
    def __init__(self, children: list[Formula]):
        super().__init__()
        self.children = children

class BinaryOperator(Operator):
    def __init__(self, left: Formula, right: Formula):
        super().__init__([left, right])
    
    def __str__(self):
        return f"({self.children[0]} {self.operator} {self.children[1]})"

class UnaryOperator(Operator):
    def __init__(self, child: Formula):
        super().__init__([child])
    
    def __str__(self):
        return f"{self.operator}({self.children[0]})"

class Not(UnaryOperator):
    operator = "¬"

    def __init__(self, child):
        super().__init__(child)

class And(BinaryOperator):
    operator = "∧"

    def __init__(self, left, right):
        super().__init__(left, right)

class Or(BinaryOperator):
    operator = "∨"

    def __init__(self, left, right):
        super().__init__(left, right)

class G(UnaryOperator):
    operator = "G"

    def __init__(self, child):
        super().__init__(child)

class F(UnaryOperator):
    operator = "F"

    def __init__(self, child):
        super().__init__(child)

class X(UnaryOperator):
    operator = "X"

    def __init__(self, child):
        super().__init__(child)

class W(UnaryOperator):
    operator = "W"

    def __init__(self, child):
        super().__init__(child)

class U(BinaryOperator):
    operator = "U"

    def __init__(self, left, right):
        super().__init__(left, right)

class AP(Formula):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def __str__(self):
        return self.name