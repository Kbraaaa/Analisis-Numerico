import math

def f(x, funcion_str):
    return eval(funcion_str)

def falsa_posicion(funcion_str, a, b, max_iter, tolerancia):
    try:
        fa = f(a, funcion_str)
        fb = f(b, funcion_str)
    except Exception as e:
        print("Error en la función:", e)
        return None

    # Validación inicial
    if fa * fb >= 0:
        print("No hay cambio de signo en el intervalo [a, b]")
        return None

    print("\nIteración\t a\t\t b\t\t c\t\t f(c)")

    for i in range(max_iter):
        # Fórmula de falsa posición
        c = b - fb * (b - a) / (fb - fa)
        fc = f(c, funcion_str)

        print(f"{i}\t\t {a:.6f}\t {b:.6f}\t {c:.6f}\t {fc:.6f}")

        # Criterio de parada
        if abs(fc) < tolerancia:
            print("\nSolución aproximada:", c)
            return c

        # Actualizar intervalo
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    print("\nSe alcanzó el número máximo de iteraciones.")
    print("Última aproximación:", c)
    return c


# --------------------------
# PROGRAMA PRINCIPAL
# --------------------------

print("=== Método de Falsa Posición ===")

funcion_str = input("Ingrese la función (ej: x**2 - 4): ")
a = float(input("Ingrese el límite inferior a: "))
b = float(input("Ingrese el límite superior b: "))
max_iter = int(input("Ingrese número máximo de iteraciones: "))
tolerancia = float(input("Ingrese tolerancia: "))

falsa_posicion(funcion_str, a, b, max_iter, tolerancia)