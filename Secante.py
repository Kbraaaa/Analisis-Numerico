import math

def f(x, funcion_str):
    return eval(funcion_str)

def metodo_secante(funcion_str, x0, x1, max_iter, tolerancia=1e-6):
    print("\nIteración\t x0\t\t x1\t\t x2\t\t Error")
    
    for i in range(max_iter):
        try:
            fx0 = f(x0, funcion_str)
            fx1 = f(x1, funcion_str)

            if fx1 - fx0 == 0:
                print("Error: División por cero")
                return None

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

            error = abs(x2 - x1)

            print(f"{i}\t\t {x0:.6f}\t {x1:.6f}\t {x2:.6f}\t {error:.6f}")

            if error < tolerancia:
                print("\nSolución aproximada:", x2)
                return x2

            # Actualizar valores
            x0 = x1
            x1 = x2

        except Exception as e:
            print("Error en la función:", e)
            return None

    print("\nSe alcanzó el número máximo de iteraciones.")
    print("Última aproximación:", x2)
    return x2


# --------------------------
# PROGRAMA PRINCIPAL
# --------------------------

print("=== Método de la Secante ===")

funcion_str = input("Ingrese la función en términos de x (ej: x**2 - 4): ")

x0 = float(input("Ingrese x0: "))
x1 = float(input("Ingrese x1: "))
max_iter = int(input("Ingrese número máximo de iteraciones: "))
tolerancia = float(input("Ingrese tolerancia (ej: 0.0001): "))

metodo_secante(funcion_str, x0, x1, max_iter, tolerancia)
