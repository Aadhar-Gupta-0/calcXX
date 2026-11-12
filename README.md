# calcXX — Scientific Desk

A standalone scientific desktop calculator with a safe arithmetic engine and a modernized, keyboard-friendly Python GUI.

## Features

- Exact decimal arithmetic for ordinary sums, subtraction, products, and division
- Operators: `+`, `-`, `*`, `/`, `//`, `%`, `**` (or `^`)
- Functions: `sqrt(x)`, `abs(x)`, `round(x, places)`, `sin(x)`, `cos(x)`, `tan(x)`, `ln(x)`, `log10(x)` (trigonometry uses radians)
- Constants: `pi`, `e`
- Last 30 calculations in memory; double-click a row to reuse it
- No `eval()`, plugins, telemetry, accounts, or network calls
- Limits on input length, expression complexity, numeric magnitude, and exponent size

## Run

Python 3.11+ is recommended. Tkinter is included with most desktop Python distributions.

```bash
python app.py
python -m unittest discover -s tests -v
```

You can also integrate the numerical core without starting a GUI:

```python
from calcxx import evaluate_expression
print(evaluate_expression("sqrt(144) + 0.1 + 0.2"))
```

## Limitations

Scientific functions use floating-point math internally; their results are approximate. Decimal precision is not a substitute for a certified numerical computation system. History is intentionally in memory, not persisted.

## Origin

This is a new standalone implementation informed by the Python desktop calculator reference [DatDevSteve/pycalc](https://github.com/DatDevSteve/pycalc). The reference project is MIT licensed and credits Steve (2025). This edition does not copy or redistribute upstream Qt-generated code, the large Windows executables, or binary assets. The new source is licensed under the repository's MIT license.
