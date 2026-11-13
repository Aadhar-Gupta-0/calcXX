"""A bounded arithmetic expression engine. No eval(), exec(), or code execution."""
from __future__ import annotations

import ast
from decimal import Decimal, DivisionByZero, InvalidOperation, localcontext
from math import cos, e, pi, sin, sqrt, tan, log, log10

MAX_EXPRESSION = 240
MAX_NODES = 80
MAX_ABS = Decimal("1e100")
MAX_POWER = 100


class CalculatorError(ValueError):
    pass


def _decimal(value: object) -> Decimal:
    try:
        result = Decimal(str(value))
        if not result.is_finite() or abs(result) > MAX_ABS:
            raise CalculatorError("Number is outside the supported range")
        return result
    except (InvalidOperation, ValueError, OverflowError) as error:
        if isinstance(error, CalculatorError):
            raise
        raise CalculatorError("Unsupported numeric value") from error


def _unary_function(name: str, value: Decimal) -> Decimal:
    if name == "abs":
        return abs(value)
    if name == "sqrt":
        if value < 0:
            raise CalculatorError("Square root requires a nonnegative value")
        return value.sqrt()
    if name == "sin":
        return _decimal(sin(float(value)))
    if name == "cos":
        return _decimal(cos(float(value)))
    if name == "tan":
        return _decimal(tan(float(value)))
    if name == "ln":
        if value <= 0:
            raise CalculatorError("Natural logarithm requires a positive value")
        return _decimal(log(float(value)))
    if name == "log10":
        if value <= 0:
            raise CalculatorError("Logarithm requires a positive value")
        return _decimal(log10(float(value)))
    raise CalculatorError("Function is not supported")


def evaluate_expression(expression: str) -> Decimal:
    """Evaluate a restricted expression using an AST and Decimal arithmetic.

    Supported: + - * / // % **, parentheses, pi/e, sqrt, sin, cos, tan, ln,
    log10, abs, round(x) or round(x, digits). Trig uses radians.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise CalculatorError("Enter a calculation")
    if len(expression) > MAX_EXPRESSION:
        raise CalculatorError("Expression is too long")
    try:
        parsed = ast.parse(expression.strip().replace("^", "**"), mode="eval")
    except (SyntaxError, ValueError) as error:
        raise CalculatorError("Invalid expression syntax") from error
    if sum(1 for _ in ast.walk(parsed)) > MAX_NODES:
        raise CalculatorError("Expression is too complex")

    def solve(node: ast.AST, depth: int = 0) -> Decimal:
        if depth > 30:
            raise CalculatorError("Expression is nested too deeply")
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return _decimal(node.value)
        if isinstance(node, ast.Name):
            if node.id == "pi":
                return _decimal(pi)
            if node.id == "e":
                return _decimal(e)
            raise CalculatorError("Unknown variable")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            a = solve(node.operand, depth + 1)
            return a if isinstance(node.op, ast.UAdd) else -a
        if isinstance(node, ast.BinOp):
            left, right = solve(node.left, depth + 1), solve(node.right, depth + 1)
            try:
                if isinstance(node.op, ast.Add):
                    value = left + right
                elif isinstance(node.op, ast.Sub):
                    value = left - right
                elif isinstance(node.op, ast.Mult):
                    value = left * right
                elif isinstance(node.op, ast.Div):
                    value = left / right
                elif isinstance(node.op, ast.FloorDiv):
                    value = left // right
                elif isinstance(node.op, ast.Mod):
                    value = left % right
                elif isinstance(node.op, ast.Pow):
                    if right != int(right) or abs(right) > MAX_POWER:
                        raise CalculatorError("Exponent must be a whole number between -100 and 100")
                    if left == 0 and right < 0:
                        raise CalculatorError("Cannot divide by zero")
                    value = left ** int(right)
                else:
                    raise CalculatorError("Operator is not supported")
            except (DivisionByZero, ZeroDivisionError, InvalidOperation, OverflowError) as error:
                raise CalculatorError("Arithmetic error: check division by zero or numerical range") from error
            return _decimal(value)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.keywords:
                raise CalculatorError("Only named calculator functions are allowed")
            name = node.func.id
            if name == "round":
                if len(node.args) not in (1, 2):
                    raise CalculatorError("round takes one or two arguments")
                value = solve(node.args[0], depth + 1)
                digits = solve(node.args[1], depth + 1) if len(node.args) == 2 else Decimal(0)
                if digits != int(digits) or abs(digits) > 30:
                    raise CalculatorError("Rounding digits must be an integer between -30 and 30")
                return _decimal(round(value, int(digits)))
            if len(node.args) != 1:
                raise CalculatorError("Functions take exactly one argument")
            return _unary_function(name, solve(node.args[0], depth + 1))
        raise CalculatorError("Expression contains an unsupported operation")

    with localcontext() as ctx:
        ctx.prec = 40
        try:
            return _decimal(solve(parsed.body))
        except (InvalidOperation, DivisionByZero, OverflowError) as error:
            raise CalculatorError("Result is outside the supported range") from error


def format_result(value: Decimal) -> str:
    if not isinstance(value, Decimal) or not value.is_finite():
        raise CalculatorError("Invalid result")
    if value == value.to_integral_value():
        return format(value, "f") if abs(value) < Decimal("1e30") else str(value.normalize())
    return format(value.normalize(), "f") if abs(value) < Decimal("1e20") else str(value.normalize())
