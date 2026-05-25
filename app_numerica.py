import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import os
from datetime import datetime

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ── Paleta de colores ─────────────────────────────────────────────────────────
C_BG       = "#1e2330"
C_PANEL    = "#252b3b"
C_CARD     = "#2d3347"
C_ACCENT   = "#4a90d9"
C_ACCENT2  = "#5ba3e8"
C_SUCCESS  = "#4caf50"
C_ERROR    = "#e57373"
C_TEXT     = "#e8eaf0"
C_SUBTEXT  = "#8a90a4"
C_BORDER   = "#3a4060"
C_ENTRY    = "#1a1f2e"
C_HOVER    = "#3a4a6b"

FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_LABEL  = ("Segoe UI", 10)
FONT_BOLD   = ("Segoe UI", 10, "bold")
FONT_MONO   = ("Consolas", 9)
FONT_RESULT = ("Consolas", 11, "bold")

# ── Entorno matemático seguro ─────────────────────────────────────────────────
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

# ── Métodos: raíces de ecuaciones ─────────────────────────────────────────────

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
            raiz = c; break
        fa = evaluar(f_expr, a)
        if fa * fc < 0:
            b = c
        else:
            a = c
    else:
        raiz = (a + b) / 2
    return raiz, tabla

def metodo_falsa_posicion(f_expr, a, b, tol, max_iter):
    fa = evaluar(f_expr, a)
    fb = evaluar(f_expr, b)
    if fa * fb >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos.")
    tabla, raiz, c_prev = [], None, None
    for i in range(1, max_iter + 1):
        fa = evaluar(f_expr, a)
        fb = evaluar(f_expr, b)
        c  = b - fb * (b - a) / (fb - fa)
        fc = evaluar(f_expr, c)
        err = abs(c - c_prev) if c_prev is not None else abs(b - a)
        err_pct = abs(err / c) * 100 if abs(c) > 1e-15 else err
        tabla.append({'iter': i, 'a': a, 'b': b, 'c': c, 'fc': fc, 'error': err_pct})
        if abs(fc) < tol or err < tol:
            raiz = c; break
        if fa * fc < 0:
            b = c
        else:
            a = c
        c_prev = c
    else:
        raiz = c
    return raiz, tabla

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
            raiz = x_new; break
        x = x_new
    else:
        raiz = x
    return raiz, tabla

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
            raiz = x2; break
        x0, x1 = x1, x2
    else:
        raiz = x1
    return raiz, tabla

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
            raiz = x_new; break
        x = x_new
    else:
        raiz = x
    return raiz, tabla

# ── Métodos: sistemas de ecuaciones lineales ──────────────────────────────────

def metodo_jacobi(A, b, x0, max_iter, tol):
    n = len(A)
    x = x0[:]
    tabla = []
    for k in range(1, max_iter + 1):
        x_new = [0.0] * n
        for i in range(n):
            if abs(A[i][i]) < 1e-15:
                raise ValueError(f"Diagonal A[{i+1}][{i+1}] = 0. Reordena el sistema.")
            s = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - s) / A[i][i]
        error = max(abs(x_new[i] - x[i]) for i in range(n))
        tabla.append({'iter': k, 'x': x_new[:], 'error': error})
        if error < tol:
            return x_new, tabla
        x = x_new
    return x, tabla

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

# ── Aplicación principal ──────────────────────────────────────────────────────

class AppNumerica(tk.Tk):

    METODOS_MATRIZ = {"Jacobi", "Gauss-Seidel"}

    def __init__(self):
        super().__init__()
        self.title("Métodos Numéricos — Análisis Numérico")
        self.geometry("1200x780")
        self.minsize(900, 620)
        self.configure(bg=C_BG)
        self._historial    = []
        self._tabla_actual = []
        self._raiz_actual  = None
        self._modo_matriz  = False
        self._n_ec         = 3
        self._mat_vars     = []   # list[list[StringVar]] para A
        self._b_vars       = []   # list[StringVar] para b
        self._x0_vars      = []   # list[StringVar] para x0
        self._build_ui()
        self._on_metodo_change()

    # ── Construcción de la UI ─────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        contenido = tk.Frame(self, bg=C_BG)
        contenido.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        contenido.columnconfigure(0, weight=0, minsize=330)
        contenido.columnconfigure(1, weight=1)
        contenido.rowconfigure(0, weight=1)

        self._panel_izq = tk.Frame(contenido, bg=C_BG)
        self._panel_izq.grid(row=0, column=0, sticky="ns", padx=(0, 8))

        self._panel_der = tk.Frame(contenido, bg=C_BG)
        self._panel_der.grid(row=0, column=1, sticky="nsew")
        self._panel_der.rowconfigure(0, weight=1)
        self._panel_der.rowconfigure(1, weight=1)
        self._panel_der.columnconfigure(0, weight=1)

        self._build_panel_entrada()
        self._build_panel_resultado()
        self._build_panel_grafica()

    def _build_header(self):
        hdr = tk.Frame(self, bg=C_ACCENT, height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  Métodos Numéricos", font=("Segoe UI", 15, "bold"),
                 bg=C_ACCENT, fg="white").pack(side="left", padx=12, pady=10)
        tk.Label(hdr,
                 text="Análisis Numérico — Ecuaciones y Sistemas Lineales",
                 font=("Segoe UI", 9), bg=C_ACCENT, fg="#cde0f5").pack(side="left")

    def _card(self, parent, title):
        outer = tk.Frame(parent, bg=C_BORDER, bd=0)
        outer.pack(fill="x", pady=(0, 8))
        inner = tk.Frame(outer, bg=C_CARD, bd=0)
        inner.pack(fill="x", padx=1, pady=1)
        tk.Label(inner, text=title, font=FONT_BOLD, bg=C_CARD,
                 fg=C_ACCENT).pack(anchor="w", padx=12, pady=(8, 4))
        tk.Frame(inner, bg=C_BORDER, height=1).pack(fill="x", padx=12)
        body = tk.Frame(inner, bg=C_CARD)
        body.pack(fill="x", padx=12, pady=8)
        return outer, body

    def _labeled_entry(self, parent, label, default="", width=28):
        row = tk.Frame(parent, bg=C_CARD)
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, font=FONT_LABEL, bg=C_CARD, fg=C_TEXT,
                 width=14, anchor="w").pack(side="left")
        var = tk.StringVar(value=default)
        ent = tk.Entry(row, textvariable=var, font=FONT_MONO, bg=C_ENTRY,
                       fg=C_TEXT, insertbackground=C_TEXT, relief="flat",
                       width=width, bd=0, highlightthickness=1,
                       highlightbackground=C_BORDER, highlightcolor=C_ACCENT)
        ent.pack(side="left", ipady=5, padx=(4, 0))
        return var, ent

    def _boton(self, parent, text, cmd, bg=C_CARD, fg=C_TEXT):
        return tk.Button(parent, text=text, command=cmd, font=FONT_BOLD,
                         bg=bg, fg=fg, activebackground=C_HOVER,
                         activeforeground="white", relief="flat",
                         cursor="hand2", pady=8, bd=0, highlightthickness=0)

    # ── Panel izquierdo ───────────────────────────────────────────────────────

    def _build_panel_entrada(self):
        # --- Método ---
        self._met_outer, card_met = self._card(self._panel_izq, "Método")
        tk.Label(card_met, text="Método numérico:", font=FONT_LABEL,
                 bg=C_CARD, fg=C_TEXT).pack(anchor="w")
        self._metodo_var = tk.StringVar(value="Bisección")
        metodos = ["Bisección", "Falsa Posición", "Newton-Raphson",
                   "Secante", "Punto Fijo", "Jacobi", "Gauss-Seidel"]
        cb = ttk.Combobox(card_met, textvariable=self._metodo_var,
                          values=metodos, state="readonly", width=26,
                          font=FONT_LABEL)
        cb.pack(anchor="w", pady=(4, 0))
        cb.bind("<<ComboboxSelected>>", lambda e: self._on_metodo_change())

        # --- Función (métodos escalares) ---
        self._func_outer, self._card_func = self._card(self._panel_izq, "Función")
        self._var_f,  self._ent_f  = self._labeled_entry(
            self._card_func, "f(x) =", "x**3 - x - 2")
        self._var_df, self._ent_df = self._labeled_entry(
            self._card_func, "f'(x) =", "3*x**2 - 1")
        self._var_g,  self._ent_g  = self._labeled_entry(
            self._card_func, "g(x) =", "")

        # --- Parámetros ---
        self._par_outer, self._card_par = self._card(self._panel_izq, "Parámetros")
        # _row_ab se oculta en modo matriz
        self._row_ab = tk.Frame(self._card_par, bg=C_CARD)
        self._row_ab.pack(fill="x")
        self._var_a, _ = self._labeled_entry(self._row_ab, "a / x₀ =", "0")
        self._var_b, _ = self._labeled_entry(self._row_ab, "b / x₁ =", "2")
        self._var_tol,  _ = self._labeled_entry(self._card_par, "Tolerancia =", "1e-6")
        self._var_iter, _ = self._labeled_entry(self._card_par, "Máx. iter. =", "100")

        # --- Sistema Lineal Ax = b (Jacobi / Gauss-Seidel) ---
        self._mat_outer, card_mat = self._card(
            self._panel_izq, "Sistema Lineal  Ax = b")
        self._mat_outer.pack_forget()   # oculto hasta que se seleccione

        n_row = tk.Frame(card_mat, bg=C_CARD)
        n_row.pack(fill="x", pady=(0, 6))
        tk.Label(n_row, text="Ecuaciones (n):", font=FONT_LABEL,
                 bg=C_CARD, fg=C_TEXT).pack(side="left")
        self._n_var = tk.StringVar(value="3")
        tk.Spinbox(n_row, from_=2, to=8, textvariable=self._n_var,
                   width=4, font=FONT_MONO, bg=C_ENTRY, fg=C_TEXT,
                   buttonbackground=C_CARD, relief="flat",
                   highlightthickness=1,
                   highlightbackground=C_BORDER).pack(side="left", padx=6)
        self._boton(n_row, "Generar", self._generar_grilla,
                    bg=C_ACCENT, fg="white").pack(side="left")

        # Canvas desplazable para la grilla de la matriz
        self._mat_canvas_frame = tk.Frame(card_mat, bg=C_CARD)
        self._mat_canvas_frame.pack(fill="x")
        self._mat_canvas = tk.Canvas(self._mat_canvas_frame, bg=C_CARD,
                                     highlightthickness=0, height=200)
        mat_vsb = ttk.Scrollbar(self._mat_canvas_frame, orient="vertical",
                                 command=self._mat_canvas.yview)
        self._mat_inner = tk.Frame(self._mat_canvas, bg=C_CARD)
        self._mat_win = self._mat_canvas.create_window(
            (0, 0), window=self._mat_inner, anchor="nw")
        self._mat_canvas.configure(yscrollcommand=mat_vsb.set)
        self._mat_canvas.pack(side="left", fill="x", expand=True)
        mat_vsb.pack(side="right", fill="y")
        self._mat_inner.bind("<Configure>",
            lambda e: self._mat_canvas.configure(
                scrollregion=self._mat_canvas.bbox("all")))
        self._mat_canvas.bind("<Configure>",
            lambda e: self._mat_canvas.itemconfig(self._mat_win, width=e.width))

        # --- Botones de acción ---
        btn_frame = tk.Frame(self._panel_izq, bg=C_BG)
        btn_frame.pack(fill="x", pady=4)
        self._boton(btn_frame, "  Resolver", self._resolver,
                    bg=C_ACCENT, fg="white").pack(fill="x", pady=(0, 6))
        self._boton(btn_frame, "  Exportar PDF", self._exportar_pdf,
                    bg=C_CARD, fg=C_TEXT).pack(fill="x", pady=(0, 6))
        self._boton(btn_frame, "  Historial", self._ver_historial,
                    bg=C_CARD, fg=C_TEXT).pack(fill="x")

        # --- Resultado rápido ---
        _, res_card = self._card(self._panel_izq, "Resultado")
        self._lbl_raiz = tk.Label(res_card, text="—", font=FONT_RESULT,
                                  bg=C_CARD, fg=C_SUCCESS,
                                  wraplength=300, justify="left")
        self._lbl_raiz.pack(anchor="w")
        self._lbl_iters = tk.Label(res_card, text="", font=FONT_LABEL,
                                   bg=C_CARD, fg=C_SUBTEXT)
        self._lbl_iters.pack(anchor="w")

        # Generar grilla inicial
        self._generar_grilla()

    def _generar_grilla(self):
        try:
            n = int(self._n_var.get())
            if not (2 <= n <= 8):
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "n debe ser entero entre 2 y 8.", parent=self)
            return

        prev_n = len(self._mat_vars)
        prev_a  = [[v.get() for v in row] for row in self._mat_vars]
        prev_b  = [v.get() for v in self._b_vars]
        prev_x0 = [v.get() for v in self._x0_vars]

        for w in self._mat_inner.winfo_children():
            w.destroy()

        self._n_ec    = n
        self._mat_vars = []
        self._b_vars   = []
        self._x0_vars  = []

        ecfg = dict(font=FONT_MONO, bg=C_ENTRY, fg=C_TEXT,
                    insertbackground=C_TEXT, relief="flat", width=7,
                    highlightthickness=1, highlightbackground=C_BORDER,
                    highlightcolor=C_ACCENT)

        # Encabezado columnas: x1..xn | b
        for j in range(n):
            tk.Label(self._mat_inner, text=f"x{j+1}", font=FONT_BOLD,
                     bg=C_CARD, fg=C_ACCENT).grid(row=0, column=j,
                                                   padx=2, pady=(0, 2))
        tk.Label(self._mat_inner, text=" | ", font=FONT_MONO,
                 bg=C_CARD, fg=C_SUBTEXT).grid(row=0, column=n, padx=1)
        tk.Label(self._mat_inner, text="b", font=FONT_BOLD,
                 bg=C_CARD, fg=C_ACCENT).grid(row=0, column=n+1, padx=2)

        # Filas de la matriz A y vector b
        for i in range(n):
            row_vars = []
            for j in range(n):
                default = prev_a[i][j] if i < prev_n and j < prev_n else "0"
                var = tk.StringVar(value=default)
                tk.Entry(self._mat_inner, textvariable=var,
                         **ecfg).grid(row=i+1, column=j, padx=2, pady=2, ipady=4)
                row_vars.append(var)
            self._mat_vars.append(row_vars)
            tk.Label(self._mat_inner, text=" | ", font=FONT_MONO,
                     bg=C_CARD, fg=C_SUBTEXT).grid(row=i+1, column=n, padx=1)
            bv = tk.StringVar(value=(prev_b[i] if i < len(prev_b) else "0"))
            tk.Entry(self._mat_inner, textvariable=bv,
                     **ecfg).grid(row=i+1, column=n+1, padx=2, pady=2, ipady=4)
            self._b_vars.append(bv)

        # Separador
        sep_row = n + 1
        tk.Frame(self._mat_inner, bg=C_BORDER, height=1).grid(
            row=sep_row, column=0, columnspan=n+2, sticky="ew", pady=6)

        # Vector x0
        tk.Label(self._mat_inner, text="Vector x₀ inicial:", font=FONT_BOLD,
                 bg=C_CARD, fg=C_TEXT).grid(row=sep_row+1, column=0,
                                             columnspan=n+2, sticky="w", pady=(0, 3))
        for j in range(n):
            xv = tk.StringVar(value=(prev_x0[j] if j < len(prev_x0) else "0"))
            tk.Entry(self._mat_inner, textvariable=xv,
                     **ecfg).grid(row=sep_row+2, column=j, padx=2, pady=2, ipady=4)
            self._x0_vars.append(xv)

        self._mat_canvas.update_idletasks()
        self._mat_canvas.configure(
            scrollregion=self._mat_canvas.bbox("all"))

        if self._modo_matriz:
            self._rebuild_tree(matrix_mode=True, n=n)

    # ── Panel derecho: tabla ──────────────────────────────────────────────────

    def _build_panel_resultado(self):
        frame = tk.Frame(self._panel_der, bg=C_PANEL, bd=0)
        frame.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Tabla de Iteraciones", font=FONT_BOLD,
                 bg=C_PANEL, fg=C_ACCENT).grid(row=0, column=0, sticky="w",
                                                padx=12, pady=(8, 4))
        self._tree_container = tk.Frame(frame, bg=C_PANEL)
        self._tree_container.grid(row=1, column=0, columnspan=2,
                                   sticky="nsew", padx=12, pady=(0, 8))
        self._tree_container.rowconfigure(0, weight=1)
        self._tree_container.columnconfigure(0, weight=1)

        self._init_tree_style()
        self._rebuild_tree(matrix_mode=False)

    def _init_tree_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Num.Treeview",
                        background=C_CARD, foreground=C_TEXT,
                        fieldbackground=C_CARD, rowheight=22,
                        font=FONT_MONO, borderwidth=0)
        style.configure("Num.Treeview.Heading",
                        background=C_ACCENT, foreground="white",
                        font=FONT_BOLD, relief="flat")
        style.map("Num.Treeview",
                  background=[("selected", C_HOVER)],
                  foreground=[("selected", "white")])

    def _rebuild_tree(self, matrix_mode=False, n=3):
        for w in self._tree_container.winfo_children():
            w.destroy()

        if matrix_mode:
            x_cols = tuple(f"x{i+1}" for i in range(n))
            cols   = ("Iter",) + x_cols + ("Error",)
            x_w    = max(70, min(110, 580 // n))
            widths = [45] + [x_w] * n + [85]
        else:
            cols   = ("Iter", "a", "b", "c (raíz)", "f(c)", "Error %")
            widths = [45, 110, 110, 110, 110, 90]

        self._tree = ttk.Treeview(self._tree_container, columns=cols,
                                   show="headings", style="Num.Treeview")
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center", minwidth=35)

        vsb = ttk.Scrollbar(self._tree_container, orient="vertical",
                             command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

    # ── Panel derecho: gráfica ────────────────────────────────────────────────

    def _build_panel_grafica(self):
        frame = tk.Frame(self._panel_der, bg=C_PANEL)
        frame.grid(row=1, column=0, sticky="nsew")
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        tk.Label(frame, text="Gráfica", font=FONT_BOLD,
                 bg=C_PANEL, fg=C_ACCENT).grid(row=0, column=0, sticky="w",
                                                padx=12, pady=(8, 4))
        self._fig = Figure(figsize=(6, 3.2), dpi=96, facecolor=C_CARD)
        self._ax  = self._fig.add_subplot(111)
        self._ax.set_facecolor(C_ENTRY)
        self._fig.subplots_adjust(left=0.09, right=0.97, top=0.92, bottom=0.14)
        self._canvas = FigureCanvasTkAgg(self._fig, master=frame)
        self._canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew",
                                          padx=12, pady=(0, 8))

    # ── Lógica dinámica de la UI ──────────────────────────────────────────────

    def _on_metodo_change(self):
        m = self._metodo_var.get()
        self._modo_matriz = m in self.METODOS_MATRIZ

        if self._modo_matriz:
            self._func_outer.pack_forget()
            self._row_ab.pack_forget()
            self._mat_outer.pack(fill="x", pady=(0, 8), after=self._par_outer)
            self._rebuild_tree(matrix_mode=True, n=self._n_ec)
        else:
            self._mat_outer.pack_forget()
            self._func_outer.pack(fill="x", pady=(0, 8), after=self._met_outer)
            # Restaurar _row_ab al principio de _card_par
            slaves = self._card_par.pack_slaves()
            if slaves:
                self._row_ab.pack(fill="x", before=slaves[0])
            else:
                self._row_ab.pack(fill="x")
            self._rebuild_tree(matrix_mode=False)

            self._ent_df.config(
                state="normal" if m == "Newton-Raphson" else "disabled")
            self._ent_g.config(
                state="normal" if m == "Punto Fijo" else "disabled")
            self._ent_f.config(state="normal")

            hints = {
                "Bisección":      ("x**3 - x - 2", "", ""),
                "Falsa Posición": ("x**3 - x - 2", "", ""),
                "Newton-Raphson": ("x**3 - x - 2", "3*x**2 - 1", ""),
                "Secante":        ("x**3 - x - 2", "", ""),
                "Punto Fijo":     ("x**3 - x - 2", "", "(x + 2)**(1/3)"),
            }
            all_f  = {h[0] for h in hints.values()}
            all_df = {h[1] for h in hints.values()}
            all_g  = {h[2] for h in hints.values()}
            fh, dfh, gh = hints.get(m, ("", "", ""))
            if not self._var_f.get() or self._var_f.get() in all_f:
                self._var_f.set(fh)
            if not self._var_df.get() or self._var_df.get() in all_df:
                self._var_df.set(dfh)
            if not self._var_g.get() or self._var_g.get() in all_g:
                self._var_g.set(gh)

    # ── Resolver ─────────────────────────────────────────────────────────────

    def _resolver(self):
        try:
            metodo  = self._metodo_var.get()
            tol     = float(self._var_tol.get())
            maxiter = int(self._var_iter.get())

            if self._modo_matriz:
                n = self._n_ec
                try:
                    A  = [[float(self._mat_vars[i][j].get())
                           for j in range(n)] for i in range(n)]
                    b  = [float(v.get()) for v in self._b_vars]
                    x0 = [float(v.get()) for v in self._x0_vars]
                except ValueError:
                    raise ValueError("Todos los valores de la matriz deben ser números.")

                if metodo == "Jacobi":
                    raiz, tabla = metodo_jacobi(A, b, x0, maxiter, tol)
                else:
                    raiz, tabla = metodo_gauss_seidel(A, b, x0, maxiter, tol)

                expr_desc = f"A({n}×{n})"

            else:
                a      = float(self._var_a.get())
                b_val  = float(self._var_b.get())
                f_expr = self._var_f.get().strip()
                df_expr= self._var_df.get().strip()
                g_expr = self._var_g.get().strip()

                if metodo in ("Bisección", "Falsa Posición",
                              "Newton-Raphson", "Secante") and not f_expr:
                    raise ValueError("Ingresa f(x).")
                if metodo == "Newton-Raphson" and not df_expr:
                    raise ValueError("Ingresa f'(x) para Newton-Raphson.")
                if metodo == "Punto Fijo" and not g_expr:
                    raise ValueError("Ingresa g(x) para Punto Fijo.")

                if metodo == "Bisección":
                    raiz, tabla = metodo_biseccion(f_expr, a, b_val, tol, maxiter)
                elif metodo == "Falsa Posición":
                    raiz, tabla = metodo_falsa_posicion(f_expr, a, b_val, tol, maxiter)
                elif metodo == "Newton-Raphson":
                    raiz, tabla = metodo_newton(f_expr, df_expr, a, tol, maxiter)
                elif metodo == "Secante":
                    raiz, tabla = metodo_secante(f_expr, a, b_val, tol, maxiter)
                elif metodo == "Punto Fijo":
                    raiz, tabla = metodo_punto_fijo(g_expr, a, tol, maxiter)

                expr_desc = f_expr or g_expr

            self._tabla_actual = tabla
            self._raiz_actual  = raiz
            self._poblar_tabla(tabla)
            self._mostrar_resultado(raiz, tabla)

            if self._modo_matriz:
                self._graficar_convergencia(metodo)
            else:
                self._graficar(f_expr,
                               g_expr if metodo == "Punto Fijo" else None,
                               a, b_val, raiz, metodo)

            self._guardar_historial(metodo, expr_desc, raiz, len(tabla))

        except Exception as ex:
            messagebox.showerror("Error", str(ex), parent=self)
            self._lbl_raiz.config(text="Error", fg=C_ERROR)

    # ── Tabla ─────────────────────────────────────────────────────────────────

    def _poblar_tabla(self, tabla):
        self._tree.delete(*self._tree.get_children())
        if not tabla:
            return
        es_matriz = 'x' in tabla[0]
        for r in tabla:
            if es_matriz:
                vals = ((r['iter'],)
                        + tuple(f"{xi:.8f}" for xi in r['x'])
                        + (f"{r['error']:.6e}",))
            else:
                vals = (r['iter'],
                        f"{r['a']:.8f}", f"{r['b']:.8f}",
                        f"{r['c']:.10f}", f"{r['fc']:.6e}",
                        f"{r['error']:.6f}")
            tag = "conv" if r is tabla[-1] else ""
            self._tree.insert("", "end", values=vals, tags=(tag,))
        self._tree.tag_configure("conv",
                                  background="#1e3a2a", foreground=C_SUCCESS)
        last = self._tree.get_children()[-1]
        self._tree.see(last)
        self._tree.selection_set(last)

    def _mostrar_resultado(self, raiz, tabla):
        if isinstance(raiz, list):
            sol = "  ".join(f"x{i+1}={v:.6f}" for i, v in enumerate(raiz))
            self._lbl_raiz.config(text=sol, fg=C_SUCCESS)
        else:
            self._lbl_raiz.config(text=f"x ≈ {raiz:.12f}", fg=C_SUCCESS)
        iters = len(tabla)
        err   = tabla[-1]['error'] if tabla else 0
        self._lbl_iters.config(
            text=f"{iters} iteraciones  |  Error: {err:.4e}")

    # ── Gráficas ──────────────────────────────────────────────────────────────

    def _ax_base(self):
        self._ax.clear()
        self._ax.set_facecolor(C_ENTRY)
        self._ax.tick_params(colors=C_SUBTEXT, labelsize=8)
        for spine in self._ax.spines.values():
            spine.set_color(C_BORDER)
        self._ax.grid(True, color=C_BORDER, linewidth=0.5,
                      linestyle="--", alpha=0.6)

    def _graficar_convergencia(self, metodo):
        self._ax_base()
        if not self._tabla_actual:
            self._canvas.draw()
            return
        iters  = [r['iter']  for r in self._tabla_actual]
        errors = [r['error'] for r in self._tabla_actual]
        import numpy as np
        errors_np = np.array(errors, dtype=float)
        errors_np = np.where(errors_np <= 0, 1e-300, errors_np)
        self._ax.semilogy(iters, errors_np, color=C_ACCENT2, linewidth=1.8,
                          marker='o', markersize=4, label="Error máx.")
        self._ax.set_xlabel("Iteración", color=C_SUBTEXT, fontsize=8)
        self._ax.set_ylabel("Error (escala log)", color=C_SUBTEXT, fontsize=8)
        self._ax.set_title(f"{metodo} — Convergencia",
                           fontsize=9, color=C_TEXT, pad=6)
        self._ax.legend(fontsize=7, facecolor=C_CARD,
                        edgecolor=C_BORDER, labelcolor=C_TEXT)
        self._canvas.draw()

    def _graficar(self, f_expr, g_expr, a, b, raiz, metodo):
        self._ax_base()
        if f_expr or g_expr:
            expr   = f_expr or g_expr
            margen = max(abs(b - a) * 0.5, 1.5)
            x_min  = min(a, b, raiz) - margen
            x_max  = max(a, b, raiz) + margen

            import numpy as np
            xs = np.linspace(x_min, x_max, 600)
            ys = []
            for xi in xs:
                try:
                    ys.append(evaluar(expr, float(xi)))
                except Exception:
                    ys.append(float('nan'))
            ys = np.where(np.abs(np.array(ys, dtype=float)) > 1e6,
                          np.nan, np.array(ys, dtype=float))

            curve_label = "f(x)" if f_expr else "g(x)"
            self._ax.plot(xs, ys, color=C_ACCENT2, linewidth=1.8,
                          label=f"{curve_label} = {expr[:40]}")
            self._ax.axhline(0, color=C_SUBTEXT, linewidth=0.8)

            if metodo in ("Bisección", "Falsa Posición"):
                self._ax.axvline(a, color="#f0c040", linewidth=1.2,
                                 linestyle="--", label=f"a={a}")
                self._ax.axvline(b, color="#f08040", linewidth=1.2,
                                 linestyle="--", label=f"b={b}")

            if raiz is not None:
                try:
                    yr = evaluar(expr, raiz)
                    self._ax.plot(raiz, yr, "o", color=C_ERROR,
                                  markersize=9, zorder=5,
                                  label=f"Raíz≈{raiz:.6f}")
                except Exception:
                    pass

            self._ax.legend(fontsize=7, facecolor=C_CARD,
                            edgecolor=C_BORDER, labelcolor=C_TEXT)
            self._ax.set_title(f"{metodo}", fontsize=9, color=C_TEXT, pad=6)
        self._canvas.draw()

    # ── Historial ─────────────────────────────────────────────────────────────

    def _guardar_historial(self, metodo, expr, raiz, iters):
        if isinstance(raiz, list):
            raiz_display = "[" + ", ".join(f"{v:.4f}" for v in raiz) + "]"
        else:
            raiz_display = raiz
        self._historial.append({
            'fecha':  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'metodo': metodo,
            'expr':   expr,
            'raiz':   raiz_display,
            'iters':  iters,
        })

    def _ver_historial(self):
        if not self._historial:
            messagebox.showinfo("Historial",
                                "No hay cálculos en el historial.", parent=self)
            return
        win = tk.Toplevel(self)
        win.title("Historial de cálculos")
        win.configure(bg=C_BG)
        win.geometry("750x380")
        cols = ("Fecha", "Método", "Función / Sistema", "Solución", "Iters.")
        style = ttk.Style(win)
        style.configure("Hist.Treeview", background=C_CARD, foreground=C_TEXT,
                        fieldbackground=C_CARD, font=FONT_MONO, rowheight=22)
        style.configure("Hist.Treeview.Heading", background=C_ACCENT,
                        foreground="white", font=FONT_BOLD)
        tree = ttk.Treeview(win, columns=cols, show="headings",
                             style="Hist.Treeview")
        for c, w in zip(cols, [155, 110, 160, 200, 50]):
            tree.heading(c, text=c)
            tree.column(c, width=w, anchor="center")
        for h in reversed(self._historial):
            raiz_val = h['raiz']
            if isinstance(raiz_val, float):
                raiz_str = f"{raiz_val:.8f}"
            else:
                raiz_str = str(raiz_val)[:30]
            tree.insert("", "end", values=(
                h['fecha'], h['metodo'], h['expr'][:30],
                raiz_str, h['iters']))
        vsb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=12)
        vsb.pack(side="right", fill="y", pady=12, padx=(0, 8))

    # ── Exportar PDF ──────────────────────────────────────────────────────────

    def _exportar_pdf(self):
        if not self._tabla_actual:
            messagebox.showwarning("Exportar",
                                   "Primero resuelve un problema.", parent=self)
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf"), ("PNG", "*.png")],
            title="Guardar resultados", parent=self)
        if not path:
            return
        try:
            from matplotlib.backends.backend_pdf import PdfPages
            import numpy as np

            metodo = self._metodo_var.get()
            raiz   = self._raiz_actual
            tabla  = self._tabla_actual
            es_mat = isinstance(raiz, list)

            raiz_str = ("[" + ", ".join(f"{v:.8f}" for v in raiz) + "]"
                        if es_mat else f"{raiz:.10f}")

            with PdfPages(path) as pdf:
                # Página 1: tabla
                fig_t, ax_t = plt.subplots(figsize=(11, 8.5))
                fig_t.patch.set_facecolor("white")
                ax_t.axis("off")
                ax_t.set_title(f"Método: {metodo}  |  Solución: {raiz_str}",
                               fontsize=12, fontweight="bold", pad=16)
                if es_mat:
                    n = len(raiz)
                    col_labels = ["Iter"] + [f"x{i+1}" for i in range(n)] + ["Error"]
                    data = [[r['iter']]
                            + [f"{xi:.8f}" for xi in r['x']]
                            + [f"{r['error']:.6e}"] for r in tabla]
                else:
                    col_labels = ["Iter", "a", "b", "c (raíz)", "f(c)", "Error %"]
                    data = [[r['iter'], f"{r['a']:.8f}", f"{r['b']:.8f}",
                             f"{r['c']:.10f}", f"{r['fc']:.6e}",
                             f"{r['error']:.6f}"] for r in tabla]
                tbl = ax_t.table(cellText=data, colLabels=col_labels,
                                 loc="center", cellLoc="center")
                tbl.auto_set_font_size(False)
                tbl.set_fontsize(8)
                tbl.scale(1, 1.4)
                for (row, col), cell in tbl.get_celld().items():
                    if row == 0:
                        cell.set_facecolor("#4a90d9")
                        cell.set_text_props(color="white", fontweight="bold")
                    elif row % 2 == 0:
                        cell.set_facecolor("#f0f4f8")
                pdf.savefig(fig_t, bbox_inches="tight")
                plt.close(fig_t)

                # Página 2: gráfica
                fig_g = Figure(figsize=(10, 6), dpi=150)
                ax_g  = fig_g.add_subplot(111)
                if es_mat:
                    iters  = [r['iter'] for r in tabla]
                    errors = np.array([r['error'] for r in tabla], dtype=float)
                    errors = np.where(errors <= 0, 1e-300, errors)
                    ax_g.semilogy(iters, errors, color="#2c6fad",
                                  linewidth=2, marker='o', markersize=4)
                    ax_g.set_xlabel("Iteración")
                    ax_g.set_ylabel("Error máx. (log)")
                    ax_g.set_title(f"{metodo} — Convergencia",
                                   fontsize=12, fontweight="bold")
                    ax_g.grid(True, linestyle="--", alpha=0.4)
                else:
                    f_expr = self._var_f.get().strip()
                    g_expr = self._var_g.get().strip()
                    expr   = f_expr or g_expr
                    a_val  = float(self._var_a.get())
                    b_val  = float(self._var_b.get())
                    if expr and not es_mat:
                        margen = max(abs(b_val - a_val) * 0.5, 1.5)
                        xs = np.linspace(min(a_val, b_val, raiz) - margen,
                                         max(a_val, b_val, raiz) + margen, 600)
                        ys = []
                        for xi in xs:
                            try: ys.append(evaluar(expr, float(xi)))
                            except: ys.append(float('nan'))
                        ys = np.array(ys, dtype=float)
                        ys = np.where(np.abs(ys) > 1e6, np.nan, ys)
                        ax_g.plot(xs, ys, color="#2c6fad", linewidth=2,
                                  label=f"f(x) = {expr[:50]}")
                        ax_g.axhline(0, color="gray", linewidth=0.8)
                        ax_g.plot(raiz, evaluar(expr, raiz), "ro",
                                  markersize=10,
                                  label=f"Raíz ≈ {raiz:.8f}")
                        ax_g.legend()
                        ax_g.set_title(f"{metodo}", fontsize=12,
                                       fontweight="bold")
                        ax_g.grid(True, linestyle="--", alpha=0.4)
                import io
                buf = io.BytesIO()
                fig_g.savefig(buf, format="png", dpi=150, bbox_inches="tight")
                buf.seek(0)
                img_fig, img_ax = plt.subplots(figsize=(10, 6))
                img_ax.imshow(plt.imread(buf))
                img_ax.axis("off")
                pdf.savefig(img_fig, bbox_inches="tight")
                plt.close(img_fig)

            messagebox.showinfo("Exportar",
                                f"Guardado en:\n{path}", parent=self)
        except ImportError:
            if path.endswith(".pdf"):
                path = path.replace(".pdf", ".png")
            self._fig.savefig(path, dpi=150, bbox_inches="tight",
                              facecolor=C_CARD)
            messagebox.showinfo("Exportar",
                                f"matplotlib-pdf no disponible.\n"
                                f"Gráfica guardada como PNG:\n{path}",
                                parent=self)
        except Exception as ex:
            messagebox.showerror("Error al exportar", str(ex), parent=self)


# ── Punto de entrada ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = AppNumerica()
    app.mainloop()
