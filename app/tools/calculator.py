import re

def parse_math_expression(expression: str):
    """
    Interpreta expressões matemáticas básicas usando regex.
    Suporta: soma (+), subtração (-), multiplicação (*) e divisão (/).
    """
    pattern = re.compile(r'(\d+)\s*([\+\-\*/])\s*(\d+)')
    match = pattern.search(expression)
    
    if not match:
        return None  # Se não encontrar expressão matemática, retorna None

    num1, operator, num2 = match.groups()
    num1, num2 = float(num1), float(num2)

    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2 if num2 != 0 else "Erro: Divisão por zero"

    return None
