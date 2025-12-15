#!/usr/bin/env python3
import re

equation = "2x+4=10"
left, right = equation.split('=', 1)
left, right = left.strip(), right.strip()

print(f"Original left: {left}")
print(f"Original right: {right}")

# Handle implicit multiplication like 2x -> 2*x
left = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', left)
print(f"After multiplication fix: {left}")

# Test with x=3
test_expr = left.replace('x', '3')
print(f"Test expression: {test_expr}")
print(f"Left result: {eval(test_expr)}")
print(f"Right result: {eval(right)}")
print(f"Equal? {eval(test_expr) == eval(right)}")
