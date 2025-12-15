#!/usr/bin/env python3
"""Test cases for the calculator"""

import sys
sys.path.append('/Users/YashB/applications')
from calc_app import calc, solve_equation, parse_natural_language, parse_fractions

def test_basic_math():
    print("=== Basic Math Tests ===")
    tests = [
        ("2+3", 5),
        ("10-4", 6),
        ("3*4", 12),
        ("15/3", 5),
        ("2^3", 8),
        ("2**3", 8),
    ]
    
    for expr, expected in tests:
        result = calc(expr)
        status = "✓" if result == expected else "✗"
        print(f"{status} {expr} = {result} (expected {expected})")

def test_fractions():
    print("\n=== Fraction Tests ===")
    tests = [
        ("1/2 + 1/3", "5/6"),
        ("3/4 - 1/4", "1/2"),
        ("2 1/2 + 1/4", "2 3/4"),
        ("1/2 * 2", 1),
    ]
    
    for expr, expected in tests:
        result = calc(expr)
        status = "✓" if str(result) == str(expected) else "✗"
        print(f"{status} {expr} = {result} (expected {expected})")

def test_natural_language():
    print("\n=== Natural Language Tests ===")
    tests = [
        ("9 squared", 81),
        ("5 cubed", 125),
        ("sqrt 16", 4.0),
    ]
    
    for expr, expected in tests:
        result = calc(expr)
        status = "✓" if result == expected else "✗"
        print(f"{status} {expr} = {result} (expected {expected})")

def test_equations():
    print("\n=== Equation Tests ===")
    tests = [
        ("2x+4=10", "x = 3"),
        ("6+x=7", "x = 1"),
        ("x^2-4=0", "x = -2 or x = 2"),
        ("5x+101010=10", "x = -20200"),
    ]
    
    for expr, expected in tests:
        result = solve_equation(expr)
        status = "✓" if result == expected else "✗"
        print(f"{status} {expr} → {result} (expected {expected})")

def test_functions():
    print("\n=== Function Tests ===")
    tests = [
        ("sqrt(16)", 4.0),
        ("sin(0)", 0.0),
        ("cos(0)", 1.0),
        ("pi", 3.141592653589793),
    ]
    
    for expr, expected in tests:
        result = calc(expr)
        status = "✓" if abs(result - expected) < 0.0001 else "✗"
        print(f"{status} {expr} = {result} (expected {expected})")

if __name__ == "__main__":
    test_basic_math()
    test_fractions()
    test_natural_language()
    test_equations()
    test_functions()
    print("\n=== Test Complete ===")
