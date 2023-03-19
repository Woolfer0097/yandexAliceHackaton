import random
import math

LEVELS = {1: "лёгкий", 2: "средний", 3: "продвинутый"}
BASE_OPERATORS = ["^", "sqrt", "*", "/", "+", "-"]
ADVANCED_OPERATORS = ["!", "log", "^"]
KEY = ("+", "-")
SQAURES = list(map(lambda x: {x: x*x}, range(1, 100)))


class Generator:
    def __init__(self, lvl: int, n: int, operators: list):
        self.level = lvl
        self.expressions_number = n
        self.operators = operators  # operator to generate
        self.operators_count = len(operators)
        self.filtered_operators = sorted(operators, key=BASE_OPERATORS.index)
        self.last_expression = ""  # default
        self.expressions_stack = []  # default

    # o_ind_p - original index plus | o_ind_m - original index minus
    # f_ind_p - filtered index plus | f_ind_m - filtered index minus
    def filter_operators(self):
        o_ind_p, o_ind_m = self.operators.index(KEY[0]), self.operators.index(KEY[1])
        f_ind_p, f_ind_m = self.filtered_operators.index(KEY[0]), self.filtered_operators.index(KEY[1])
        self.filtered_operators[min(f_ind_p, f_ind_m)], self.filtered_operators[max(f_ind_p, f_ind_m)] = \
            self.operators[min(o_ind_p, o_ind_m)], self.operators[max(o_ind_p, o_ind_m)]
        return self.filtered_operators

    def generate_sum_expr(self):
        rll = 1  # range_limit_left
        rlr = 10 ** self.level  # range_limit_right
        if self.operators_count == len(self.filtered_operators):
            n1, n2 = random.randint(rll, rlr), random.randint(rll, rlr)
            return f"{n1} + {n2}"
        else:
            return f"{self.last_expression} + {random.randint(rll, rlr)}"

    def generate_sub_expr(self):
        rll = 10 ** self.level  # range_limit_left
        rlr = 1  # range_limit_right
        if self.operators_count == len(self.filtered_operators):
            n1, n2 = random.randint(rlr, rll), random.randint(rlr, rll)
            return f"{n1} - {n2}"
        else:
            rll = eval(self.last_expression)
            return f"{self.last_expression} - {random.randint(rlr, rll)}"

    def generate_mul_expr(self):
        rll = 1  # range_limit_left
        rlr = 10 * self.level  # range_limit_right
        if self.operators_count == len(self.filtered_operators):
            n1, n2 = random.randint(rll, rlr), random.randint(rll, rlr)
            return f"{n1} * {n2}"
        else:
            rll = eval(self.last_expression)
            return f"{self.last_expression} * {random.randint(rll, rlr)}"

    def generate_div_expr(self):
        rll = random.randint(3, 8) ** self.level  # range_limit_left
        if self.operators_count == len(self.filtered_operators):
            rlr = random.choice([i for i in range(2, rll) if rll % i == 0])
            n1, n2 = random.randint(rlr, rll), random.randint(rlr, rll)
            return f"{n1} / {n2}"
        else:
            rll = eval(self.last_expression)
            dividers = [i for i in range(2, rll) if rll % i == 0]
            while len(dividers) < 1:
                self.last_expression = "(" + self.last_expression
                self.last_expression += f" + {random.randint(1, 10)}"
                self.last_expression += ")"
                rll = eval(self.last_expression)
                dividers = [i for i in range(2, rll) if rll % i == 0]
            divider = random.choice(dividers)
            return f"{self.last_expression} / {divider}"

    def generate_pow_expr(self):
        r = 10 * self.level  # range of list of squares
        if self.operators_count == len(self.filtered_operators):
            n1 = random.randint(1, r)
            return f"{n1} ** {2}"
        else:
            value = eval(self.last_expression)
            if value >= 100:
                self.last_expression += f" - {random.randint(value // 2, value + 1)}"
            return f"{self.last_expression} ** {2}"

    def generate_sqrt_expr(self):
        r = (self.level ** 5)
        r = 100 if (r > 100) else 100  # range of list of squares
        index = random.randint(1, r)
        number = SQAURES[index]
        return [f"√{number}", index]

    def generate(self):
        while self.filtered_operators:
            match self.filtered_operators[0]:
                case "^":
                    self.last_expression = self.generate_pow_expr()
                case "sqrt":
                    self.last_expression = self.generate_sqrt_expr()
                case "*":
                    self.last_expression = self.generate_mul_expr()
                case "/":
                    self.last_expression = self.generate_div_expr()
                case "+":
                    self.last_expression = self.generate_sum_expr()
                case "-":
                    self.last_expression = self.generate_sub_expr()
            self.filtered_operators.pop(0)
        return [self.last_expression, int(eval(self.last_expression))]


if __name__ == '__main__':
    level = 1
    n = 5
    for _ in range(n):
        gen = Generator(level, n, ["*", "/", "+", "-"])
        gen_output = gen.generate()
        expression, answer = gen_output[0], gen_output[1]
        print(f"LEVEL: {level} | EXPRESSION: {expression} ANSWER: {answer}")
    print()
    print()
    level = 2
    n = 5
    for _ in range(n):
        gen = Generator(level, n, ["*", "/", "+", "-"])
        gen_output = gen.generate()
        expression, answer = gen_output[0], gen_output[1]
        print(f"LEVEL: {level} | EXPRESSION: {expression} ANSWER: {answer}")
    print()
    print()
    level = 3
    n = 5
    for _ in range(n):
        gen = Generator(level, n, ["*", "/", "+", "-"])
        gen_output = gen.generate()
        expression, answer = gen_output[0], gen_output[1]
        print(f"LEVEL: {level} | EXPRESSION: {expression} ANSWER: {answer}")
