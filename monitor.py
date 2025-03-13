from formula import *
from eval_tables import eval_tables, Verdict

class MonitoredFormula:
    def __init__(self, formula: Formula, mode: str):
        self.formula = formula
        self.mode = mode
    
    def __str__(self):
        return f"R[{self.formula}]{self.mode}"

class Evaluation:
    def __init__(self, formula: MonitoredFormula, verdict: Verdict):
        self.formula = formula
        self.verdict = verdict

class Monitor:
    def __initFN(self, phi: Formula):
        match phi:
            case AP(name=name):
                self.requests.append(MonitoredFormula(phi, ""))
            case Not(children=[child]):
                self.__initFN(child)
                self.requests.append(MonitoredFormula(phi, ""))
            case BinaryOperator(children=[left, right]):
                self.__initFN(left)
                self.__initFN(right)
                self.requests.append(MonitoredFormula(phi, ""))
            case G(children=[child]):
                self.__initFN(child)
                self.requests.append(MonitoredFormula(phi, ""))
            case F(children=[child]):
                self.__initFN(child)
                self.requests.append(MonitoredFormula(phi, ""))
            case X(children=[child]):
                self.requests.append(MonitoredFormula(phi, ""))
            case W(children=[child]):
                self.requests.append(MonitoredFormula(phi, ""))


    def __init__(self, formula: Formula):
        self.formula = formula
        self.requests = []
        self.evaluations = []
        self.__initFN(formula)

    def __get_eval(self, formula: Formula):
        for eval in self.evaluations:
            if eval.formula.formula == formula:
                return eval.verdict
        raise ValueError("Evaluation not found")
    
    def step(self, observations: list[str]):
        # Apply evaluation rules
        self.evaluations = []
        for req in self.requests:
            match req.formula:
                case AP(name=name):
                    self.evaluations.append(Evaluation(req, (Verdict.TRUE if name in observations else Verdict.FALSE, '')))
                case BinaryOperator(children=[left, right]):
                    eval_table = eval_tables[type(req.formula)][req.mode]
                    if req.mode == "l":
                        self.evaluations.append(Evaluation(req, eval_table[self.__get_eval(left)[0]]))
                    elif req.mode == "r":
                        self.evaluations.append(Evaluation(req, eval_table[self.__get_eval(right)[0]]))
                    else:
                        self.evaluations.append(Evaluation(req, eval_table[self.__get_eval(left)[0]][self.__get_eval(right)[0]]))
                case UnaryOperator(children=[child]):
                    eval_table = eval_tables[type(req.formula)][req.mode]
                    self.evaluations.append(Evaluation(req, eval_table[self.__get_eval(child)[0]]))
                case _:
                    raise ValueError("Invalid formula")

        # Apply reactivation rules
        self.requests = []
        for eval in self.evaluations:
            if eval.verdict[0] == Verdict.UNKNOWN_TRUE or eval.verdict[0] == Verdict.UNKNOWN_FALSE:
                match eval.formula.formula:
                    case Not(children=[child]):
                        self.requests.append(MonitoredFormula(eval.formula.formula, ""))
                    case And(children=[left, right]) | Or(children=[left, right]):
                        self.requests.append(MonitoredFormula(eval.formula.formula, eval.verdict[1]))
                    case G(children=[child]) | F(children=[child]):
                        self.__initFN(child)
                        self.requests.append(MonitoredFormula(eval.formula.formula, ""))
                    case X(children=[child]) | W(children=[child]):
                        if eval.formula.mode == "":
                            self.__initFN(child)
                        self.requests.append(MonitoredFormula(eval.formula.formula, eval.verdict[1]))
                    case U(children=[left, right]):
                        self.__initFN(left)
                        self.__initFN(right)
                        self.requests.append(MonitoredFormula(eval.formula.formula, eval.verdict[1]))
                    case _:
                        raise ValueError("Invalid formula")

if __name__ == "__main__":
    phi = G(Or(Not(AP("distance")), F(AP("stop"))))
    print(phi)
    mon = Monitor(phi)
    print(list(map(str, mon.requests)))
    
    for aps in [[], ["distance"], ["stop"]]:
        print(aps)
        mon.step(aps)
        print(list(map(lambda x: str(x.formula) + ": "+ str(x.verdict), mon.evaluations)))
        print(list(map(str, mon.requests)))
        print()