from formula import *
from eval_tables import eval_tables, Verdict
from ordered_set import OrderedSet
import graphviz

class MonitoredFormula:
    def __init__(self, formula, mode, step=0, depends_on=[]):
        self.formula = formula
        self.mode = mode
        self.step = step
        self.depends_on = set(depends_on)
    
    def __str__(self):
        return "R{}[{}]{}".format(self.step, self.formula, self.mode)

    def __eq__(self, other):
        return self.formula == other.formula and self.step == other.step
    
    def __hash__(self):
        return hash((self.formula, self.step))

class Evaluation:
    def __init__(self, formula, verdict):
        self.formula = formula
        self.verdict = verdict

def append_and_return(li, item):
    li.append(item)
    return item

class Monitor:
    def __initFN(self, phi, step=0, update_or_insert=None):
        if update_or_insert == None:
            update_or_insert = lambda x: append_and_return(self.requests, x)
        appended = []
        if isinstance(phi, AP):
            appended.append(update_or_insert(MonitoredFormula(phi, "", step)))
        elif isinstance(phi, Not):
            appended.append(update_or_insert(MonitoredFormula(phi, "", step, self.__initFN(phi.children[0], step, update_or_insert))))
        elif isinstance(phi, BinaryOperator):
            appended.append(update_or_insert(MonitoredFormula(phi, "", step, self.__initFN(phi.children[0], step, update_or_insert) + self.__initFN(phi.children[1], step, update_or_insert))))
        elif isinstance(phi, G) or isinstance(phi, F):
            appended.append(update_or_insert(MonitoredFormula(phi, "", step, self.__initFN(phi.children[0], step, update_or_insert))))
        elif isinstance(phi, X) or isinstance(phi, W):
            appended.append(update_or_insert(MonitoredFormula(phi, "", step)))
        else:
            raise ValueError("Invalid formula")
        return appended

    def __init__(self, formula):
        self.formula = formula
        self.requests = OrderedSet()
        self.evaluations = []
        self.__initFN(formula)

    def __get_eval(self, req, formula):
        for eval in self.evaluations:
            if eval.formula in req.depends_on and eval.formula.formula == formula:
                return eval.verdict
        raise ValueError("Evaluation not found")

    def __insert_or_replace_eval(self, eval):
        for i in range(len(self.evaluations)):
            if self.evaluations[i].formula.formula == eval.formula.formula:
                self.evaluations[i] = eval
                return
        self.evaluations.append(eval)
    
    def to_dot(self):
        res = graphviz.Digraph()
        for request in self.requests:
            res.node(str(request), str(request))
            for dep in request.depends_on:
                res.edge(str(request), str(dep))
        return res

    def step(self, observations):
        # Apply evaluation rules
        # import ipdb; ipdb.set_trace()
        for req in self.requests:
            if isinstance(req.formula, AP):
                self.__insert_or_replace_eval(Evaluation(req, (Verdict.TRUE if req.formula.name in observations else Verdict.FALSE, '')))
            elif isinstance(req.formula, BinaryOperator):
                eval_table = eval_tables[type(req.formula)][req.mode]
                if req.mode == "L":
                    self.__insert_or_replace_eval(Evaluation(req, eval_table[self.__get_eval(req, req.formula.children[0])[0]]))
                elif req.mode == "R":
                    self.__insert_or_replace_eval(Evaluation(req, eval_table[self.__get_eval(req, req.formula.children[1])[0]]))
                else:
                    self.__insert_or_replace_eval(Evaluation(req, eval_table[self.__get_eval(req, req.formula.children[0])[0]][self.__get_eval(req, req.formula.children[1])[0]]))
            elif isinstance(req.formula, (X, W)):
                eval_table = eval_tables[type(req.formula)][req.mode]
                if req.mode == '':
                    self.__insert_or_replace_eval(Evaluation(req, eval_tables[type(req.formula)][req.mode]))
                else:
                    self.__insert_or_replace_eval(Evaluation(req, eval_table[self.__get_eval(req, req.formula.children[0])[0]]))
            elif isinstance(req.formula, G):
                self.__insert_or_replace_eval(Evaluation(req, ((Verdict.UNKNOWN_TRUE if all(map(lambda x: self.__get_eval(req, x.formula)[0] == Verdict.TRUE, req.depends_on))
                                                              else (Verdict.FALSE if any(map(lambda x: self.__get_eval(req, x.formula)[0] == Verdict.FALSE, req.depends_on))
                                                                    else Verdict.UNKNOWN_FALSE)), "")))
            elif isinstance(req.formula, F):
                self.__insert_or_replace_eval(
                    Evaluation(req, (Verdict.TRUE if any(map(lambda x: self.__get_eval(req, x.formula)[0] == Verdict.TRUE, req.depends_on)) else Verdict.UNKNOWN_FALSE), ""))
            elif isinstance(req.formula, UnaryOperator):
                eval_table = eval_tables[type(req.formula)][req.mode]
                self.__insert_or_replace_eval(Evaluation(req, eval_table[self.__get_eval(req, req.formula.children[0])[0]]))
            else:
                raise ValueError("Invalid formula")

        # Apply reactivation rules
        old_requests = self.requests
        self.requests = OrderedSet()
        def update_or_insert(f):
            if f not in old_requests:
                self.requests.add(f)
                return f
            else:
                for req in old_requests:
                    if req == f:
                        self.requests.add(req)
                        req.mode = f.mode
                        req.depends_on = f.depends_on
                        return req
        for eval in self.evaluations:
            if eval.verdict[0] == Verdict.UNKNOWN_TRUE or eval.verdict[0] == Verdict.UNKNOWN_FALSE:
                if isinstance(eval.formula.formula, Not):
                    update_or_insert(MonitoredFormula(eval.formula.formula, "", eval.formula.step, eval.formula.depends_on))
                elif isinstance(eval.formula.formula, (And, Or)):
                    # import ipdb; ipdb.set_trace()
                    update_or_insert(MonitoredFormula(eval.formula.formula, eval.verdict[1], eval.formula.step, eval.formula.depends_on))
                elif isinstance(eval.formula.formula, (G, F)):
                    new_inits = self.__initFN(eval.formula.formula.children[0], eval.formula.step + 1, update_or_insert)
                    update_or_insert(MonitoredFormula(eval.formula.formula, "", eval.formula.step + 1, eval.formula.depends_on.union(new_inits)))
                elif isinstance(eval.formula.formula, (X, W)):
                    depends = eval.formula.depends_on
                    if eval.formula.mode == "":
                        depends = depends.union(self.__initFN(eval.formula.formula.children[0], eval.formula.step + 1))
                    update_or_insert(MonitoredFormula(eval.formula.formula, eval.verdict[1], eval.formula.step, depends))
                elif isinstance(eval.formula.formula, U):
                    self.__initFN(eval.formula.formula.children[0], 0, update_or_insert)
                    self.__initFN(eval.formula.formula.children[1], 0, update_or_insert)
                    update_or_insert(MonitoredFormula(eval.formula.formula, eval.verdict[1]))
                else:
                    raise ValueError("Invalid formula")

def rep_op(op, num):
    if num == 1:
        return op
    else:
        def inner(x):
            return rep_op(op, num - 1)(op(x))
        return inner
        

if __name__ == "__main__":
    phi = G(Or(AP('a'), rep_op(X, 1)(AP('b'))))
    print(phi)
    mon = Monitor(phi)
    print(map(str, mon.requests))
    n = 0

    for aps in [[], ['a', 'b'], ['a']]:
        print(aps)
        dg = mon.to_dot()
        dg.name = "Step " + str(n)
        dg.view(directory="/tmp")
#        raw_input("Press Enter to continue...")
        mon.step(aps)
        print(map(lambda x: str(x.formula) + ": " + str(x.verdict[0]) + x.verdict[1], mon.evaluations))
        print(map(str, mon.requests))
        print()
        n += 1