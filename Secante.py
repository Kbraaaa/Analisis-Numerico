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

def metodo_secante(f_expr, x0, x1, tol, max_iter):
    tabla, raiz = [], None
    for i in range(1, max_iter + 1):
        fx0 = evaluar(f_expr, x0)
        fx1 = evaluar(f_expr, x1)
        if abs(fx1 - fx0) < 1e-15:
            raise ValueError("División por cero (f(x1) - f(x0) ≈ 0).")
        x2  = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        err = abs(x2 - x1)
        err_pct = abs(err / x2) * 100 if abs(x2) > 1e-15 else err
        tabla.append({'iter': i, 'a': x0, 'b': x1, 'c': x2,
                      'fc': evaluar(f_expr, x2), 'error': err_pct})
        if err < tol:
            raiz = x2
            break
        x0, x1 = x1, x2
    else:
        raiz = x1
    return raiz, tabla


if __name__ == "__main__":
    print("=== Método de la Secante ===")
    f_expr = input("Ingrese f(x) (ej: x**3 - x - 2): ").strip()
    x0     = float(input("x₀ = "))
    x1     = float(input("x₁ = "))
    tol    = float(input("Tolerancia (ej: 1e-6): "))
    niter  = int(input("Máx. iteraciones: "))

    raiz, tabla = metodo_secante(f_expr, x0, x1, tol, niter)

    print(f"\n{'Iter':>4}  {'x0':>14}  {'x1':>14}  {'x2':>16}  {'f(x2)':>12}  {'Error%':>10}")
    print("─" * 76)
    for r in tabla:
        print(f"{r['iter']:>4}  {r['a']:>14.8f}  {r['b']:>14.8f}  "
              f"{r['c']:>16.10f}  {r['fc']:>12.6e}  {r['error']:>10.6f}")
    print(f"\nRaíz aproximada: {raiz:.10f}")
