#!/usr/bin/env python3
import re
import math
from fractions import Fraction

variables = {}
meme_mode = False

def parse_natural_language(expr):
    # Convert natural language to math expressions
    expr = expr.lower()
    
    # Handle "X squared", "X cubed", etc.
    expr = re.sub(r'(\d+(?:\.\d+)?)\s+squared', r'(\1)**2', expr)
    expr = re.sub(r'(\d+(?:\.\d+)?)\s+cubed', r'(\1)**3', expr)
    expr = re.sub(r'sqrt\s+of\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    expr = re.sub(r'square\s+root\s+of\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    
    # Handle "sqrt X" without parentheses
    expr = re.sub(r'sqrt\s+(\d+(?:\.\d+)?)', r'sqrt(\1)', expr)
    
    return expr

def parse_fractions(expr):
    # Convert mixed fractions like 2 1/2 to improper fractions
    def mixed_fraction_replacer(match):
        whole, num, den = match.groups()
        improper_num = int(whole) * int(den) + int(num)
        return f'Fraction({improper_num}, {den})'
    
    # Handle mixed fractions first (e.g., "2 1/2")
    expr = re.sub(r'(\d+)\s+(\d+)/(\d+)', mixed_fraction_replacer, expr)
    
    # Convert regular fractions like 1/2, 3/4 to Fraction objects
    def fraction_replacer(match):
        num, den = match.groups()
        return f'Fraction({num}, {den})'
    
    # Replace remaining fractions in the expression
    expr = re.sub(r'(\d+)/(\d+)', fraction_replacer, expr)
    return expr

def solve_equation(equation):
    # Handle equations like 6+x=7, 2*x-3=5, etc.
    if '=' not in equation:
        return None
    
    left, right = equation.split('=', 1)
    left, right = left.strip(), right.strip()
    
    # Find the variable (single letter)
    var_match = re.search(r'[a-zA-Z]', left)
    if not var_match:
        return None
    
    var = var_match.group()
    
    # Handle implicit multiplication like 2x -> 2*x
    left = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', left)
    
    # Handle x^2 notation by converting to **2
    left = re.sub(r'([a-zA-Z])\^(\d+)', r'\1**\2', left)
    
    try:
        # Try algebraic solving for linear equations first
        # For equations like ax + b = c, solve as x = (c - b) / a
        if '**2' not in left and '*' in left:
            # Try to extract coefficient and constant
            try:
                # Test with x=0 to get constant term
                const_expr = left.replace(var, '0')
                b = eval(const_expr)
                
                # Test with x=1 to get coefficient + constant
                coeff_expr = left.replace(var, '1')
                a_plus_b = eval(coeff_expr)
                a = a_plus_b - b
                
                c = eval(right)
                
                if a != 0:
                    solution = (c - b) / a
                    if abs(solution - round(solution)) < 0.0001:
                        return f"{var} = {int(round(solution))}"
                    else:
                        frac = Fraction(solution).limit_denominator(10000)
                        if abs(float(frac) - solution) < 0.0001:
                            if frac.denominator == 1:
                                return f"{var} = {frac.numerator}"
                            else:
                                return f"{var} = {frac.numerator}/{frac.denominator}"
                        else:
                            return f"{var} = {solution:.6f}"
            except:
                pass
        
        # Fallback to brute force for smaller ranges
        for test_val in range(-100000, 100001):
            try:
                test_expr = left.replace(var, str(test_val))
                left_result = eval(test_expr)
                right_result = eval(right)
                if abs(left_result - right_result) < 0.0001:
                    return f"{var} = {test_val}"
            except:
                continue
        
        # Try Newton-Raphson for cubic equations
        if '**3' in left:
            try:
                # Newton-Raphson method: x_new = x_old - f(x)/f'(x)
                def f(x_val):
                    expr = f"({left}) - ({right})"
                    return eval(expr.replace(var, str(x_val)))
                
                def df(x_val):
                    # Numerical derivative
                    h = 0.0001
                    return (f(x_val + h) - f(x_val - h)) / (2 * h)
                
                # Start with initial guess
                x = 0.0
                for _ in range(50):  # Max 50 iterations
                    fx = f(x)
                    if abs(fx) < 0.0001:  # Close enough to zero
                        if abs(x - round(x)) < 0.0001:
                            return f"{var} = {int(round(x))}"
                        else:
                            return f"{var} = {x:.6f}"
                    
                    dfx = df(x)
                    if abs(dfx) < 0.0001:  # Avoid division by zero
                        break
                    
                    x_new = x - fx / dfx
                    if abs(x_new - x) < 0.0001:  # Converged
                        if abs(x_new - round(x_new)) < 0.0001:
                            return f"{var} = {int(round(x_new))}"
                        else:
                            return f"{var} = {x_new:.6f}"
                    x = x_new
            except:
                pass
        for whole in range(-50, 51):
            for frac_part in [0.5, 0.25, 0.75, 1/3, 2/3]:
                for test_val in [whole + frac_part, whole - frac_part]:
                    try:
                        test_expr = left.replace(var, str(test_val))
                        left_result = eval(test_expr)
                        right_result = eval(right)
                        if abs(left_result - right_result) < 0.0001:
                            frac = Fraction(test_val).limit_denominator(1000)
                            if frac.denominator == 1:
                                return f"{var} = {frac.numerator}"
                            else:
                                return f"{var} = {frac.numerator}/{frac.denominator}"
                    except:
                        continue
                
    except:
        pass
    
    return "Could not solve equation"

def calc(expr):
    # Parse natural language first
    expr = parse_natural_language(expr)
    
    # Parse fractions
    expr = parse_fractions(expr)
    
    # Convert ^ to ** for exponentiation
    expr = re.sub(r'(\d+(?:\.\d+)?|\w+)\^(\d+(?:\.\d+)?|\w+)', r'\1**\2', expr)
    
    # Add math functions to the namespace
    safe_dict = {
        '__builtins__': {},
        'sqrt': math.sqrt,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'pi': math.pi,
        'e': math.e,
        'Fraction': Fraction
    }
    
    # Replace variables with values
    for name, value in variables.items():
        expr = expr.replace(name, str(value))
    
    try:
        result = eval(expr, safe_dict)
        if str(result) == 'inf':
            return "Invalid - Division by zero"
        elif str(result) == 'nan':
            return "Invalid - Not a number"
        
        # Format fraction results nicely
        if isinstance(result, Fraction):
            if result.denominator == 1:
                return result.numerator
            else:
                # Convert to mixed fraction if improper
                if abs(result.numerator) > result.denominator:
                    whole = result.numerator // result.denominator
                    remainder = abs(result.numerator) % result.denominator
                    if remainder == 0:
                        return whole
                    else:
                        return f"{whole} {remainder}/{result.denominator}"
                else:
                    return f"{result.numerator}/{result.denominator}"
        
        return result
    except ZeroDivisionError:
        return "Invalid - Division by zero"
    except NameError as e:
        return f"Invalid - Unknown variable: {str(e).split(chr(39))[1]}"
    except SyntaxError:
        return "Invalid - Syntax error"
    except ValueError as e:
        return f"Invalid - Value error: {str(e)}"
    except:
        return "Invalid - Math error"

print("Simple Calculator - Type math expressions or 'quit'")
print("Set variables: x=5")
print("Use in math: x+3, 2*x, etc.")
print("Solve equations: 6+x=7, 2*x-3=5")
print("Functions: sqrt(16), 9**2, sin(pi/2)")
print("Natural language: '9 squared', 'sqrt of 16', '5 cubed'")
print("Fractions: 1/2 + 1/3, 2 1/2 + 3/4")
print("Type 'meme' to toggle meme mode!")

while True:
    try:
        line = input("\n> ").strip()
        
        if line == 'quit':
            break
        elif line == 'meme':
            meme_mode = not meme_mode
            status = "ON 😂" if meme_mode else "OFF"
            print(f"Meme mode: {status}")
        elif '=' in line and re.search(r'[a-zA-Z]', line):
            # Equation solving (any equation with a letter)
            result = solve_equation(line)
            print(result)
        elif '=' in line and not any(op in line.split('=')[0] for op in ['+','-','*','/']):
            # Variable assignment
            name, value = line.split('=', 1)
            variables[name.strip()] = float(value.strip())
            print(f"Set {name.strip()} = {value.strip()}")
        else:
            # Math expression
            if meme_mode and line.strip() == '9+10':
                print("= 21 😂")
            elif meme_mode and line.strip() == '2+2':
                print("= 5 (quick maths)")
            elif meme_mode and line.strip() == '1+1':
                print("= 11 (big brain)")
            elif meme_mode and line.strip() == '67':
                print("= THE MEME NUMBER 67! 🔥")
            elif meme_mode and line.strip() == '41':
                print("= 41! The answer to everything (almost) 🤔")
            elif meme_mode and '67' in line.strip():
                result = calc(line)
                print(f"= {result} (contains the legendary 67! 🔥)")
            elif meme_mode and '41' in line.strip():
                result = calc(line)
                print(f"= {result} (contains 41! 🤔)")
            else:
                result = calc(line)
                print(f"= {result}")
            
    except KeyboardInterrupt:
        break
    except:
        print("Error - try again")
