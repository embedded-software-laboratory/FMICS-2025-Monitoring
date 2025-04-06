from formula import *
from eval_tables import eval_tables, Verdict
from ordered_set import OrderedSet
import graphviz

class MonitoredFormula:
    def init_fn(self):
        if isinstance(self.formula, (AP, X, W)):
            pass # Request for the formula itself is implicit and no subrequests are created
        elif isinstance(self.formula, BinaryOperator):
            self.depends_on = [MonitoredFormula(self.formula.children[0]).init_fn(), MonitoredFormula(self.formula.children[1]).init_fn()]
        elif isinstance(self.formula, UnaryOperator): # Remaining UnaryOperators are F, G and Not
            self.depends_on = [MonitoredFormula(self.formula.children[0]).init_fn()]
        return self

    def __init__(self, formula):
        self.formula = formula
        self.mode = ""
        self.depends_on = []
        self.verdict = ("_", "") # Never evaluated

    def __find_eval(self, formula):
        for f in self.depends_on:
            if f.formula == formula:
                return f

    def get_verdict(self):
        return self.verdict[0]

    def evaluate(self, aps):
        if self.get_verdict() in [Verdict.TRUE, Verdict.FALSE]: # If the evaluation is already final, no need to check again
            return
        for x in self.depends_on:
            x.evaluate(aps)
        if isinstance(self.formula, AP):
            self.verdict = (Verdict.TRUE if self.formula.name in aps else Verdict.FALSE, "")
        elif isinstance(self.formula, BinaryOperator):
            eval_table = eval_tables[type(self.formula)][self.mode]
            if self.mode == "L":
                self.verdict= eval_table[self.__find_eval(self.formula.children[0]).get_verdict()]
            elif self.mode == "R":
                self.verdict = eval_table[self.__find_eval(self.formula.children[1]).get_verdict()]
            else:
                self.verdict = eval_table[self.__find_eval(self.formula.children[0]).get_verdict()][self.__find_eval(self.formula.children[1]).get_verdict()]
        elif isinstance(self.formula, (X, W)):
            eval_table = eval_tables[type(self.formula)][self.mode]
            if self.mode == "":
                self.verdict = eval_table
            else:
                self.verdict = eval_table[self.__find_eval(self.formula.children[0]).get_verdict()]
        elif isinstance(self.formula, G):
            child_evals = map(lambda x: x.get_verdict(), self.depends_on)
            self.verdict = (Verdict.FALSE if any(map(lambda x: x == Verdict.FALSE, child_evals)) else (
                Verdict.UNKNOWN_TRUE if all(map(lambda x: x == Verdict.TRUE, child_evals))
                else Verdict.UNKNOWN_FALSE), "")
        elif isinstance(self.formula, F):
            child_evals = map(lambda x: x.get_verdict(), self.depends_on)
            self.verdict = (Verdict.TRUE if any(map(lambda x: x == Verdict.TRUE, child_evals)) else Verdict.UNKNOWN_FALSE, "")
        elif isinstance(self.formula, UnaryOperator): # Not
            eval_table = eval_tables[type(self.formula)][self.mode]
            self.verdict = eval_table[self.__find_eval(self.formula.children[0]).get_verdict()]

    def reactivate(self):
        if self.get_verdict() in [Verdict.UNKNOWN_FALSE, Verdict.UNKNOWN_TRUE]:
            for x in self.depends_on:
                x.reactivate()
            if isinstance(self.formula, (Not, And, Or)):
                pass # Like in the init function the self reactivation is implicit
            elif isinstance(self.formula, (X, W)):
                if self.mode == "": # We're moving to "M"
                    self.depends_on = [MonitoredFormula(self.formula.children[0]).init_fn()]
            elif isinstance(self.formula, (F, G)):
                self.depends_on.append(MonitoredFormula(self.formula.children[0]).init_fn())
            elif isinstance(self.formula, U):
                self.depends_on.append(MonitoredFormula(self.formula.children[0]).init_fn())
                self.depends_on.append(MonitoredFormula(self.formula.children[1]).init_fn())

            self.mode = self.verdict[1] # Change to the required mode
        else:
            self.depends_on = []

    def __str__(self):
        return "R[{}]{}{}".format(self.formula, self.mode, self.verdict)

    def __eq__(self, other):
        return self.formula == other.formula
    
    def __hash__(self):
        return hash(self.formula)

    def __iter__(self):
        for dependent in self.depends_on:
            for x in dependent:
                yield x
        yield self

def append_and_return(li, item):
    li.append(item)
    return item

class Monitor:

    def step(self, aps):
        self.root.evaluate(aps)
        self.root.reactivate()

    def __init__(self, formula):
        self.root = MonitoredFormula(formula).init_fn()

    def get_verdict(self):
        return self.root.get_verdict()

    def __str__(self):
        return str(map(str, self))

    def __iter__(self):
        return self.root.__iter__()

    def to_dot(self):
        res = graphviz.Digraph()
        for x in self:
            res.node(str(x), str(x))
            for dep in x.depends_on:
                res.edge(str(x), str(dep))
        return res


def rep_op(op, num):
    if num == 1:
        return op
    else:
        def inner(x):
            return rep_op(op, num - 1)(op(x))
        return inner

def random_aps(aps = ["dist", "stop"]):
    import random
    random.seed(42)
    while True:
        res = []
        for x in aps:
            if random.random() < 0.5:
                res.append(x)
        yield res

if __name__ == "__main__":
    phi = G(Implies(AP('dist'), F(AP('stop'))))
    mon = Monitor(phi)
    for aps in random_aps():
        print(aps)
        mon.step(aps)
        # mon.to_dot().view()
        print(mon.get_verdict())
        if mon.get_verdict() in [Verdict.FALSE, Verdict.TRUE]:
            break