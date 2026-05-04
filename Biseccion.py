import math

def f(x, funcion_str):
    return eval(funcion_str)

def biseccion(funcion_str, a, b, max_iter, tolerancia):
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
        c = (a + b) / 2
        fc = f(c, funcion_str)

        print(f"{i}\t\t {a:.6f}\t {b:.6f}\t {c:.6f}\t {fc:.6f}")

        # Criterio de parada
        if abs(fc) < tolerancia:
            print("\nSolución aproximada:", c)
            return c

        # Decidir el nuevo intervalo
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

print("=== Método de Bisección ===")

funcion_str = input("Ingrese la función (ej: x**2 - 4): ")
a = float(input("Ingrese el límite inferior a: "))
b = float(input("Ingrese el límite superior b: "))
max_iter = int(input("Ingrese número máximo de iteraciones: "))
tolerancia = float(input("Ingrese tolerancia: "))

biseccion(funcion_str, a, b, max_iter, tolerancia)