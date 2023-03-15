import random
import math


LEVELS = {1: "лёгкий", 2: "средний", 3: "продвинутый"}
OPERATORS = ["+", "-", "//", "*", "%", "**", "!", "sqrt", "fig", "log"]  # операторы fig - для генерации графика фигуры
FIGURES = ["oval", "parabola", "sqrt"]


# Генерирует уравнение графика фигуры (окружности, параболы, корня...)
def generate_figure_equation():
    pass


def generate_plus_expr(lvl):
    n1, n2 = 0, 0
    if lvl == 1:
        n1, n2 = random.randint(1, 10), random.randint(1, 10)
    elif lvl == 2:
        n1, n2 = random.randint(1, 100), random.randint(1, 100)
    elif lvl == 3:
        n1, n2 = random.randint(1, 1000), random.randint(1, 1000)
    return f"{n1} + {n2}"


def generate_minus_expr(lvl):
    n1, n2 = 0, 0
    if lvl == 1:
        n1, n2 = random.randint(6, 10), random.randint(1, 6)
    elif lvl == 2:
        n1, n2 = random.randint(60, 100), random.randint(1, 60)
    elif lvl == 3:
        n1, n2 = random.randint(600, 1000), random.randint(1, 600)
    return f"{n1} - {n2}"


def generate_multiple_expr(lvl):
    n1, n2 = 0, 0
    if lvl == 1:
        n1, n2 = random.randint(1, 10), random.randint(1, 10)
    elif lvl in [2, 3]:
        n1, n2 = random.randint(1, 100), random.randint(1, 100)
    return f"{n1} * {n2}"


def generate_divide_expr(lvl):
    n1, n2 = 0, 0
    if lvl == 1:
        n1 = random.randint(5, 100)
        n2 = random.choice([i for i in range(1, n1) if n1 % i == 0])
    elif lvl in [2, 3]:
        n1 = random.randint(100, 1000)
        n2 = random.choice([i for i in range(1, n1 + 1) if n1 % i == 0])
    return f"{n1} / {n2}"


def generate_expression(level, operator="+"):
    match operator:
        case "+":
            return generate_plus_expr(level)
        case "-":
            return generate_minus_expr(level)
        case "*":
            return generate_multiple_expr(level)
        case "//":
            return generate_divide_expr(level)
        case "fig":
            return generate_figure_equation()


def solve_simple_expression(expr):
    return eval(expr)


def get_age():
    age = int(input())
    return age


def determine_user_level(u_age):
    if u_age < 12:
        level = 1
    elif 12 <= u_age <= 16:
        level = 2
    else:
        level = 3
    return level


def practise(u_age):
    user_level = determine_user_level(u_age)
    if user_level == 1:
        op = random.choice(OPERATORS[0:4])  # генерируем оператор
    elif user_level == 2:
        op = random.choice(OPERATORS[5:7])  # генерируем оператор
    else:
        op = random.choice(OPERATORS[7:])
    expr = generate_expression(user_level, op)
    return expr


if __name__ == '__main__':
    user_age = get_age()
    print(practise(user_age))
