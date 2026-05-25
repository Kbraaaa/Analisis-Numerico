import math

MATH_ENV = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'exp': math.exp, 'log': math.log, 'log10': math.log10,
    'log2': math.log2, 'sqrt': math.sqrt, 'abs': abs,
    'pi': math.pi, 'e': math.e,
    'ceil': math.ceil, 'floor': math.floor,
}

def evaluar(expr, x):
    env = {'x': x, '__builtins__': {}}
    env.update(MATH_ENV)
    return eval(expr, env)

def metodo_biseccion(f_expr, a, b, tol, max_iter):
    fa = evaluar(f_expr, a)
    fb = evaluar(f_expr, b)
    if fa * fb >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    tabla, raiz = [], None
    for i in range(1, max_iter + 1):
        c  = (a + b) / 2
        fc = evaluar(f_expr, c)
        err = abs((b - a) / 2)
        err_pct = abs(err / c) * 100 if abs(c) > 1e-15 else err
        tabla.append({'iter': i, 'a': a, 'b': b, 'c': c, 'fc': fc, 'error': err_pct})
        if abs(fc) < tol or err < tol:
            raiz = c
            break
        fa = evaluar(f_expr, a)
        if fa * fc < 0:
            b = c
        else:
            a = c
    else:
        raiz = (a + b) / 2
    return raiz, tabla


if __name__ == "__main__":
    print("=== Método de Bisección ===")
    f_expr = input("Ingrese f(x) (ej: x**3 - x - 2): ").strip()
    a      = float(input("a = "))
    b      = float(input("b = "))
    tol    = float(input("Tolerancia (ej: 1e-6): "))
    niter  = int(input("Máx. iteraciones: "))

    raiz, tabla = metodo_biseccion(f_expr, a, b, tol, niter)

    print(f"\n{'Iter':>4}  {'a':>14}  {'b':>14}  {'c':>16}  {'f(c)':>12}  {'Error%':>10}")
    print("─" * 76)
    for r in tabla:
        print(f"{r['iter']:>4}  {r['a']:>14.8f}  {r['b']:>14.8f}  "
              f"{r['c']:>16.10f}  {r['fc']:>12.6e}  {r['error']:>10.6f}")
    print(f"\nRaíz aproximada: {raiz:.10f}")
