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

def derivar_expr(expr_str):
    import sympy as sp
    x = sp.Symbol('x')
    expr_sym = sp.sympify(expr_str, locals={'x': x})
    deriv = sp.diff(expr_sym, x)
    resultado = str(deriv)
    resultado = resultado.replace('Abs(', 'abs(')
    return resultado

def metodo_newton(f_expr, df_expr, x0, tol, max_iter):
    tabla, raiz = [], None
    x = x0
    for i in range(1, max_iter + 1):
        fx  = evaluar(f_expr, x)
        dfx = evaluar(df_expr, x)
        if abs(dfx) < 1e-15:
            raise ValueError(f"f'(x) ≈ 0 en x={x:.6f}. Prueba otro x₀.")
        x_new = x - fx / dfx
        err = abs(x_new - x)
        err_pct = abs(err / x_new) * 100 if abs(x_new) > 1e-15 else err
        tabla.append({'iter': i, 'a': x, 'b': x_new, 'c': x_new,
                      'fc': evaluar(f_expr, x_new), 'error': err_pct})
        if err < tol:
            raiz = x_new
            break
        x = x_new
    else:
        raiz = x
    return raiz, tabla


if __name__ == "__main__":
    print("=== Método de Newton-Raphson ===")
    f_expr = input("Ingrese f(x) (ej: x**3 - x - 2): ").strip()

    auto = input("¿Calcular f'(x) automáticamente? (s/n): ").strip().lower()
    if auto == 's':
        df_expr = derivar_expr(f_expr)
        print(f"f'(x) = {df_expr}")
    else:
        df_expr = input("Ingrese f'(x): ").strip()

    x0    = float(input("x₀ = "))
    tol   = float(input("Tolerancia (ej: 1e-6): "))
    niter = int(input("Máx. iteraciones: "))

    raiz, tabla = metodo_newton(f_expr, df_expr, x0, tol, niter)

    print(f"\n{'Iter':>4}  {'x_n':>16}  {'x_n+1':>16}  {'f(x_n+1)':>14}  {'Error%':>10}")
    print("─" * 68)
    for r in tabla:
        print(f"{r['iter']:>4}  {r['a']:>16.10f}  {r['c']:>16.10f}  "
              f"{r['fc']:>14.6e}  {r['error']:>10.6f}")
    print(f"\nRaíz aproximada: {raiz:.10f}")
