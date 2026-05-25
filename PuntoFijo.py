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

def metodo_punto_fijo(g_expr, x0, tol, max_iter):
    tabla, raiz = [], None
    x = x0
    for i in range(1, max_iter + 1):
        x_new = evaluar(g_expr, x)
        err = abs(x_new - x)
        err_pct = abs(err / x_new) * 100 if abs(x_new) > 1e-15 else err
        tabla.append({'iter': i, 'a': x, 'b': x_new, 'c': x_new,
                      'fc': x_new - x, 'error': err_pct})
        if err < tol:
            raiz = x_new
            break
        x = x_new
    else:
        raiz = x
    return raiz, tabla


if __name__ == "__main__":
    print("=== Método de Punto Fijo ===")
    print("Reescribe f(x)=0 como x = g(x) e ingresa g(x).")
    g_expr = input("Ingrese g(x) (ej: (x + 2)**(1/3)): ").strip()
    x0     = float(input("x₀ = "))
    tol    = float(input("Tolerancia (ej: 1e-6): "))
    niter  = int(input("Máx. iteraciones: "))

    raiz, tabla = metodo_punto_fijo(g_expr, x0, tol, niter)

    print(f"\n{'Iter':>4}  {'x_n':>18}  {'g(x_n)':>18}  {'Error%':>12}")
    print("─" * 58)
    for r in tabla:
        print(f"{r['iter']:>4}  {r['a']:>18.10f}  {r['c']:>18.10f}  {r['error']:>12.6f}")
    print(f"\nRaíz aproximada: {raiz:.10f}")
