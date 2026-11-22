"""Safe calculator expression evaluation without eval()."""
import ast
import math
import operator

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Mod: operator.mod, ast.Pow: operator.pow}
UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def calculate(expression: str) -> str:
    if not expression or not expression.strip():
        return '0'
    expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
    if len(expression) > 160:
        raise ValueError('Expression too long')
    try:
        tree = ast.parse(expression, mode='eval')
        result = _evaluate(tree.body)
        if isinstance(result, complex) or not math.isfinite(result):
            raise ValueError('Result out of range')
        if abs(result) > 1e15:
            raise ValueError('Result too large')
        return str(int(result)) if result == int(result) else format(result, '.10g')
    except ZeroDivisionError:
        raise ValueError('Cannot divide by zero') from None
    except (SyntaxError, OverflowError, TypeError):
        raise ValueError('Invalid expression') from None


def _evaluate(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        if abs(node.value) > 1e15:
            raise ValueError('Number too large')
        return node.value
    if isinstance(node, ast.UnaryOp) and type(node.op) in UNARY:
        return UNARY[type(node.op)](_evaluate(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        a, b = _evaluate(node.left), _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and (abs(b) > 12 or abs(a) > 1e6):
            raise ValueError('Power too large')
        return OPS[type(node.op)](a, b)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'sqrt' and len(node.args) == 1 and not node.keywords:
        x = _evaluate(node.args[0])
        if x < 0:
            raise ValueError('Cannot square root a negative number')
        return math.sqrt(x)
    raise ValueError('Invalid expression')
