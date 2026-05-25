"""
╔══════════════════════════════════════════════════════╗
║         MÉTODO NUMÉRICO DE NEWTON-RAPHSON           ║
║         Resolvedor General de Ecuaciones            ║
╚══════════════════════════════════════════════════════╝

  Fórmula de iteración:
                  f(x_n)
    x_{n+1} = x_n ─────────
                  f'(x_n)
"""

import math

# ─── Funciones matemáticas disponibles para el usuario ───────────────────────
FUNCIONES_DISPONIBLES = {
    'sin': math.sin,  'cos': math.cos,  'tan': math.tan,
    'asin': math.asin,'acos': math.acos,'atan': math.atan,
    'sinh': math.sinh,'cosh': math.cosh,'tanh': math.tanh,
    'exp': math.exp,  'log': math.log,  'log10': math.log10,
    'log2': math.log2,'sqrt': math.sqrt,'abs': abs,
    'pi': math.pi,    'e': math.e,
    'ceil': math.ceil,'floor': math.floor,
}


def evaluar(expresion: str, x: float) -> float:
    """Evalúa una expresión en x de forma segura."""
    entorno = {'x': x, '__builtins__': {}}
    entorno.update(FUNCIONES_DISPONIBLES)
    return eval(expresion, entorno)


# ─── Método principal ─────────────────────────────────────────────────────────

def newton_raphson(f_expr: str, df_expr: str, x0: float,
                   iteraciones: int, tolerancia: float = 1e-10):
    """
    Aplica el método de Newton-Raphson para encontrar raíces de f(x) = 0.

    Parámetros:
        f_expr     : expresión de f(x)  como string
        df_expr    : expresión de f'(x) como string
        x0         : valor inicial (semilla)
        iteraciones: número máximo de iteraciones
        tolerancia : criterio de parada por error relativo (%)

    Retorna:
        dict con raíz, iteraciones realizadas, convergencia, error y tabla
    """
    tabla       = []
    x_actual    = x0
    convergencia = False
    raiz        = None
    error       = None

    print("\n" + "═" * 78)
    print(f"  MÉTODO DE NEWTON-RAPHSON")
    print(f"  f(x)  = {f_expr}")
    print(f"  f'(x) = {df_expr}")
    print("═" * 78)
    print(f"  {'Iter':>5}  {'x_n':>16}  {'f(x_n)':>16}  {'f\'(x_n)':>16}  {'Error':>14}")
    print("─" * 78)

    for i in range(1, iteraciones + 1):

        # ── Evaluar f y f' ────────────────────────────────────────────────────
        try:
            f_val  = evaluar(f_expr,  x_actual)
            df_val = evaluar(df_expr, x_actual)
        except Exception as e:
            print(f"\n  ⚠  Error al evaluar en x = {x_actual:.10f}: {e}")
            break

        # ── Detectar derivada nula (división por cero) ────────────────────────
        if abs(df_val) < 1e-15:
            print(f"\n  ⚠  f'(x) ≈ 0 en x = {x_actual:.10f}  →  división por cero. "
                  "Prueba con otro x₀.")
            break

        # ── Fórmula de Newton ─────────────────────────────────────────────────
        x_nuevo = x_actual - f_val / df_val

        # ── Error relativo (%) ────────────────────────────────────────────────
        if abs(x_nuevo) > 1e-15:
            error = abs((x_nuevo - x_actual) / x_nuevo) * 100
        else:
            error = abs(x_nuevo - x_actual)

        tabla.append({
            'iteracion': i,
            'x_n'      : x_actual,
            'f_x'      : f_val,
            'df_x'     : df_val,
            'x_nuevo'  : x_nuevo,
            'error'    : error,
        })

        # ── Convergencia: imprimir fila y salir de inmediato ──────────────────
        if error < tolerancia:
            print(f"  {i:>5}  {x_actual:>16.10f}  {f_val:>16.8f}  "
                  f"{df_val:>16.8f}  {error:>13.8f}%")
            convergencia = True
            raiz = x_nuevo
            break

        print(f"  {i:>5}  {x_actual:>16.10f}  {f_val:>16.8f}  "
              f"{df_val:>16.8f}  {error:>13.8f}%")
        x_actual = x_nuevo

    else:
        raiz = x_actual

    print("═" * 78)

    # ── Mensaje de resultado muy visible ──────────────────────────────────────
    if convergencia:
        iter_conv = len(tabla)
        print(f"""
  ╔{'═'*54}╗
  ║  CONVERGENCIA ALCANZADA                          ║
  ║  ►  Se detuvo en la iteración {iter_conv:<3} de {iteraciones:<3}              ║
  ║  ►  Razón: error < tolerancia ({tolerancia:.0e})            ║
  ╚{'═'*54}╝""")
    else:
        print(f"""
  ╔{'═'*54}╗
  ║  ⚠   LÍMITE DE ITERACIONES ALCANZADO                ║
  ║  ►  Se ejecutaron las {iteraciones:<3} iteraciones pedidas      ║
  ║  ►  El método NO convergió con esta tolerancia      ║
  ╚{'═'*54}╝""")

    if raiz is not None:
        try:
            f_raiz = evaluar(f_expr, raiz)
            print(f"  ➤  Raíz aproximada : x  ≈ {raiz:.10f}")
            print(f"  ➤  Comprobación    : f(x) ≈ {f_raiz:.2e}  (idealmente ≈ 0)")
        except Exception:
            pass
    if error is not None:
        print(f"  ➤  Error final     : {error:.2e} %")
    print()

    return {
        'raiz'                : raiz,
        'iteraciones_realizadas': len(tabla),
        'convergencia'        : convergencia,
        'error_final'         : error,
        'tabla'               : tabla,
    }


# ─── Entrada del usuario ──────────────────────────────────────────────────────

def mostrar_bienvenida():
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║         MÉTODO DE NEWTON-RAPHSON  —  Python                           ║
║                                                                        ║
║   Resuelve  f(x) = 0  usando la tangente como aproximación            ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

  Funciones disponibles:
    Trigonométricas : sin, cos, tan, asin, acos, atan
    Hiperbólicas    : sinh, cosh, tanh
    Exponencial/Log : exp, log, log10, log2
    Otras           : sqrt, abs, ceil, floor
    Constantes      : pi, e

  Ejemplos  (f(x)  →  f'(x)):
    ► x**3 - x - 2          →  3*x**2 - 1
    ► cos(x) - x            →  -sin(x) - 1
    ► exp(x) - 3*x          →  exp(x) - 3
    ► x**2 - 2              →  2*x            (√2)
    ► log(x) - 1            →  1/x            (x = e)
    ► x*sin(x) - 1          →  sin(x) + x*cos(x)
    """)


def pedir_expresion(nombre: str, ejemplo: str) -> str:
    """Pide una expresión al usuario y valida su sintaxis."""
    while True:
        expr = input(f"  Ingrese {nombre} (ej: {ejemplo}): ").strip()
        if not expr:
            print("  ⚠  La expresión no puede estar vacía.\n")
            continue
        try:
            evaluar(expr, 1.0)
            return expr
        except ZeroDivisionError:
            return expr   # Puede ser válida en otros puntos
        except Exception as e:
            print(f"  ⚠  Expresión inválida: {e}\n")


def pedir_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(f"  {mensaje}: ").strip())
        except ValueError:
            print("  ⚠  Ingrese un número válido.\n")


def pedir_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            n = int(input(f"  {mensaje}: ").strip())
            if n > 0:
                return n
            print("  ⚠  Debe ser un número entero positivo.\n")
        except ValueError:
            print("  ⚠  Ingrese un número entero válido.\n")


# ─── Programa principal ───────────────────────────────────────────────────────

def main():
    mostrar_bienvenida()

    while True:
        print("─" * 72)
        print("  NUEVO EJERCICIO — NEWTON-RAPHSON")
        print("─" * 72)

        f_expr  = pedir_expresion("f(x)",  "x**3 - x - 2")
        df_expr = pedir_expresion("f'(x)", "3*x**2 - 1")
        x0          = pedir_float("Valor inicial x₀")
        iteraciones = pedir_entero_positivo("Número máximo de iteraciones")

        tol_input = input("  Tolerancia (Enter = 1e-10 por defecto): ").strip()
        tolerancia = float(tol_input) if tol_input else 1e-10

        newton_raphson(f_expr, df_expr, x0, iteraciones, tolerancia)

        continuar = input("  ¿Desea resolver otro ejercicio? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n  ¡Hasta luego! 👋\n")
            break


if __name__ == "__main__":
    main()