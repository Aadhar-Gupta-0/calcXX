import unittest
from decimal import Decimal
from calcxx import CalculatorError, evaluate_expression
from calcxx.engine import format_result
from calcxx.history import History


class EngineTests(unittest.TestCase):
    def test_exact_decimal_math(self):
        self.assertEqual(evaluate_expression("0.1+0.2"), Decimal("0.3"))
        self.assertEqual(evaluate_expression("(12-3)*2"), Decimal(18))
        self.assertEqual(evaluate_expression("2^8"), Decimal(256))

    def test_division_and_modulo(self):
        self.assertEqual(evaluate_expression("10/4"), Decimal("2.5"))
        self.assertEqual(evaluate_expression("11//3"), Decimal(3))
        self.assertEqual(evaluate_expression("11%3"), Decimal(2))

    def test_functions(self):
        self.assertEqual(evaluate_expression("sqrt(81)"), Decimal(9))
        self.assertEqual(evaluate_expression("abs(-3)"), Decimal(3))
        self.assertEqual(evaluate_expression("round(1.234,2)"), Decimal("1.23"))
        self.assertEqual(evaluate_expression("sin(0)"), Decimal(0))
        self.assertEqual(evaluate_expression("log10(100)"), Decimal(2))

    def test_constants_and_formatting(self):
        self.assertTrue(Decimal("3.14") < evaluate_expression("pi") < Decimal("3.15"))
        self.assertEqual(format_result(evaluate_expression("2+2")), "4")

    def test_invalid_operations(self):
        invalid = ["1/0", "sqrt(-1)", "ln(0)", "2**9999", "2**2.5",
                   "not_a_variable", "open('secret')", "().__class__",
                   "[1,2,3]", "__import__('os').system('id')",
                   "10 if True else 0", "", "1" * 241]
        for expression in invalid:
            with self.subTest(expression=expression[:35]):
                with self.assertRaises(CalculatorError):
                    evaluate_expression(expression)

    def test_depth_and_complexity(self):
        for expression in ("1+" * 85 + "1", "(" * 40 + "1" + ")" * 40):
            with self.assertRaises(CalculatorError):
                evaluate_expression(expression)

    def test_history_capacity_and_clear(self):
        history = History()
        for n in range(40):
            history.record(str(n), str(n + 1))
        self.assertEqual(len(history.items), 30)
        self.assertEqual(history.items[0], ("39", "40"))
        history.clear()
        self.assertFalse(history.items)


if __name__ == "__main__":
    unittest.main()
