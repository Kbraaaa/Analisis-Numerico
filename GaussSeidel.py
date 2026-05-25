def metodo_gauss_seidel(A, b, x0, max_iter, tol):
    n = len(A)
    x = x0[:]
    tabla = []
    for k in range(1, max_iter + 1):
        x_new = x[:]
        for i in range(n):
            if abs(A[i][i]) < 1e-15:
                raise ValueError(f"Diagonal A[{i+1}][{i+1}] = 0. Reordena el sistema.")
            s = sum(A[i][j] * x_new[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        error = max(abs(x_new[i] - x[i]) for i in range(n))
        tabla.append({'iter': k, 'x': x_new[:], 'error': error})
        if error < tol:
            return x_new, tabla
        x = x_new
    return x, tabla


if __name__ == "__main__":
    print("=== Método de Gauss-Seidel ===")
    n = int(input("Número de ecuaciones: "))

    A = []
    print("Ingrese la matriz A fila por fila (valores separados por espacio):")
    for i in range(n):
        fila = list(map(float, input(f"  Fila {i+1}: ").split()))
        A.append(fila)

    b  = list(map(float, input("Vector b (separado por espacio): ").split()))
    x0 = list(map(float, input("Vector inicial x0 (separado por espacio): ").split()))
    tol    = float(input("Tolerancia (ej: 1e-6): "))
    niter  = int(input("Máx. iteraciones: "))

    sol, tabla = metodo_gauss_seidel(A, b, x0, niter, tol)

    print(f"\n{'Iter':>4}  {'Solución':<{n*12}}  {'Error':>12}")
    print("─" * (4 + n * 12 + 16))
    for r in tabla:
        x_str = "  ".join(f"{v:>10.6f}" for v in r['x'])
        print(f"{r['iter']:>4}  {x_str}  {r['error']:>12.6e}")
    print("\nSolución aproximada:")
    for i, v in enumerate(sol):
        print(f"  x{i+1} = {v:.10f}")
