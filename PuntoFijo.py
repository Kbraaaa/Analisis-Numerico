"""
╔══════════════════════════════════════════════════════╗
║         MÉTODO NUMÉRICO DE PUNTO FIJO               ║
║         Resolvedor General de Ecuaciones            ║
╚══════════════════════════════════════════════════════╝
"""

import math
import re


FUNCIONES_DISPONIBLES = {
    'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
    'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
    'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
    'exp': math.exp, 'log': math.log, 'log10': math.log10,
    'log2': math.log2, 'sqrt': math.sqrt, 'abs': abs,
    'pi': math.pi, 'e': math.e,
    'ceil': math.ceil, 'floor': math.floor,
}


def evaluar_funcion(expresion: str, x: float) -> float:
    """Evalúa g(x) de forma segura con el valor de x dado."""
    entorno = {'x': x, '__builtins__': {}}
    entorno.update(FUNCIONES_DISPONIBLES)
    return eval(expresion, entorno)


def punto_fijo(g_expr: str, x0: float, iteraciones: int, tolerancia: float = 1e-10):
    """
    Aplica el método de punto fijo para encontrar la raíz de f(x) = 0,
    reescrita como x = g(x).

    Parámetros:
        g_expr     : expresión de g(x) como string
        x0         : valor inicial (semilla)
        iteraciones: número máximo de iteraciones
        tolerancia : criterio de parada por error relativo

    Retorna:
        dict con resultados y tabla de iteraciones
    """
    tabla = []
    x_actual = x0
    convergencia = False
    raiz = None
    error = None

    print("\n" + "═" * 70)
    print(f"  MÉTODO DE PUNTO FIJO   |   g(x) = {g_expr}")
    print("═" * 70)
    print(f"  {'Iter':>5}  {'x_n':>18}  {'g(x_n)':>18}  {'Error':>18}")
    print("─" * 70)

    for i in range(1, iteraciones + 1):
        try:
            x_nuevo = evaluar_funcion(g_expr, x_actual)
        except Exception as e:
            print(f"\n  Error al evaluar g(x) en x = {x_actual:.10f}: {e}")
            break

        # Error relativo (evita división por cero)
        if abs(x_nuevo) > 1e-15:
            error = abs((x_nuevo - x_actual) / x_nuevo) * 100
        else:
            error = abs(x_nuevo - x_actual)

        tabla.append({
            'iteracion': i,
            'x_n': x_actual,
            'g_x': x_nuevo,
            'error': error,
        })

        if error < tolerancia:
            print(
                f"  {i:>5}  {x_actual:>18.10f}  {x_nuevo:>18.10f}  {error:>17.8f}%")
            convergencia = True
            raiz = x_nuevo
            break

        print(f"  {i:>5}  {x_actual:>18.10f}  {x_nuevo:>18.10f}  {error:>17.8f}%")
        x_actual = x_nuevo
    else:
        raiz = x_actual

    print("═" * 70)

    if convergencia:
        iter_conv = len(tabla)
        print(f"""
  ╔{'═'*50}╗
  ║    CONVERGENCIA ALCANZADA                      ║
  ║  ►  Se detuvo en la iteración {iter_conv:<3} de {iteraciones:<3}          ║
  ║  ►  Razón: error < tolerancia ({tolerancia:.0e})        ║
  ╚{'═'*50}╝""")
    else:
        print(f"""
  ╔{'═'*50}╗
  ║    LÍMITE DE ITERACIONES ALCANZADO            ║
  ║  ►  Se ejecutaron las {iteraciones} iteraciones pedidas  ║
  ║  ►  El método NO convergió con esta tolerancia  ║
  ╚{'═'*50}╝""")

    print(f"  ➤  Raíz aproximada : x ≈ {raiz:.10f}")
    print(
        f"  ➤  g(raíz)         : g(x) ≈ {evaluar_funcion(g_expr, raiz):.10f}")
    if error is not None:
        print(f"  ➤  Error final     : {error:.2e} %")
    print()

    return {
        'raiz': raiz,
        'iteraciones_realizadas': len(tabla),
        'convergencia': convergencia,
        'error_final': error,
        'tabla': tabla,
    }


def mostrar_bienvenida():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║         MÉTODO NUMÉRICO DE PUNTO FIJO  —  Python                ║
║                                                                  ║
║   Resuelve  f(x) = 0  reescribiendo la ecuación como  x = g(x)  ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

  Funciones disponibles:
    Trigonométricas : sin, cos, tan, asin, acos, atan
    Hiperbólicas    : sinh, cosh, tanh
    Exponencial/Log : exp, log, log10, log2
    Otras           : sqrt, abs, ceil, floor
    Constantes      : pi, e

  Ejemplos de g(x):
    ► cos(x)                   → de  f(x) = x - cos(x)
    ► (x**2 + 2) / 3           → de  f(x) = x² - 3x + 2
    ► exp(-x)                  → de  f(x) = x - e^(-x)
    ► (x + 5/x) / 2            → raíz cuadrada de 5 (método Heron)
    ► sqrt(10 - x**3) / 2      → de  f(x) = x³ + 2x - 10
    """)


def pedir_funcion() -> str:
    while True:
        expr = input("  Ingrese g(x) [la función de iteración]: ").strip()
        if not expr:
            print(" La expresión no puede estar vacía.\n")
            continue

        try:
            evaluar_funcion(expr, 1.0)
            return expr
        except ZeroDivisionError:
            return expr
        except Exception as e:
            print(f" Expresión inválida: {e}\n")


def pedir_float(mensaje: str) -> float:
    while True:
        try:
            return float(input(f"  {mensaje}: ").strip())
        except ValueError:
            print(" Ingrese un número válido.\n")


def pedir_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            n = int(input(f"  {mensaje}: ").strip())
            if n > 0:
                return n
            print(" Debe ser un número entero positivo.\n")
        except ValueError:
            print(" Ingrese un número entero válido.\n")


def main():
    mostrar_bienvenida()

    while True:
        print("─" * 68)
        print("  NUEVA ITERACIÓN DE PUNTO FIJO")
        print("─" * 68)

        g_expr = pedir_funcion()
        x0 = pedir_float("Valor inicial x₀")
        iteraciones = pedir_entero_positivo("Número máximo de iteraciones")

        tol_input = input("  Tolerancia (Enter = 1e-10 por defecto): ").strip()
        tolerancia = float(tol_input) if tol_input else 1e-10

        resultado = punto_fijo(g_expr, x0, iteraciones, tolerancia)

        continuar = input(
            "  ¿Desea resolver otro ejercicio? (s/n): ").strip().lower()
        if continuar != 's':
            print("\n  Gracias por usar el método de punto fijo. \n")
            break


if __name__ == "__main__":
    main()
