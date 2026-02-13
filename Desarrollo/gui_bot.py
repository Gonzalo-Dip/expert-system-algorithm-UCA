from pathlib import Path
from pyswip import Prolog
import tkinter as tk
from tkinter import ttk, messagebox
import math

# -------------------------
# Helpers
# -------------------------
def to_atom(name: str) -> str:
    s = name.strip().lower().replace(" ", "_")
    s = "".join(ch for ch in s if ch.isalnum() or ch == "_")
    if not s:
        raise ValueError("Nombre inválido")
    return s

def euclid(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def assert_distances(prolog: Prolog, coords: dict):
    # limpia dist/3 anteriores
    list(prolog.query("retractall(dist(_,_,_))"))

    nodes = list(coords.keys())
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            d = euclid(coords[a], coords[b])
            prolog.assertz(f"dist({a},{b},{d})")
            prolog.assertz(f"dist({b},{a},{d})")

def query_one(prolog: Prolog, q: str):
    res = list(prolog.query(q))
    return res[0] if res else None

def fmt_value(v):
    try:
        return str(v)
    except Exception:
        return repr(v)

def fmt_exp(exp):
    # PySwip devuelve Exp como algo printable; lo dejamos prolijo
    s = fmt_value(exp)
    return s.replace("', '", "'\n  '").replace("[", "[\n  ").replace("]", "\n]")

# -------------------------
# GUI
# -------------------------
class ExpertBotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Expert System Bot - Interfaz")
        self.root.geometry("980x640")

        # Prolog init
        self.prolog = Prolog()
        base_dir = Path(__file__).resolve().parent  # Desarrollo/
        route_motor = base_dir / "route_motor.pl"
        try:
            self.prolog.consult(str(route_motor))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar route_motor.pl:\n{e}")
            raise

        # Tabs
        nb = ttk.Notebook(root)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_entrega = ttk.Frame(nb)
        self.tab_tsp = ttk.Frame(nb)

        nb.add(self.tab_entrega, text="Entrega (plan_entrega)")
        nb.add(self.tab_tsp, text="Ruta TSP (resolver_tsp)")

        self._build_entrega_tab()
        self._build_tsp_tab()

    # -------------------------
    # Entrega Tab
    # -------------------------
    def _build_entrega_tab(self):
        frm = ttk.Frame(self.tab_entrega)
        frm.pack(fill="both", expand=True)

        left = ttk.LabelFrame(frm, text="Datos de la encomienda")
        left.pack(side="left", fill="y", padx=10, pady=10)

        # Inputs
        ttk.Label(left, text="Peso (kg)").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.e_peso = ttk.Entry(left, width=20)
        self.e_peso.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(left, text="Monto ($)").grid(row=1, column=0, sticky="w", padx=6, pady=6)
        self.e_monto = ttk.Entry(left, width=20)
        self.e_monto.grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(left, text="Zona").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        self.cb_zona = ttk.Combobox(left, values=["centro", "fuera_centro"], state="readonly", width=18)
        self.cb_zona.grid(row=2, column=1, padx=6, pady=6)
        self.cb_zona.set("centro")

        ttk.Label(left, text="Hora de carga").grid(row=3, column=0, sticky="w", padx=6, pady=6)
        self.cb_hora = ttk.Combobox(left, values=["antes_16", "despues_16"], state="readonly", width=18)
        self.cb_hora.grid(row=3, column=1, padx=6, pady=6)
        self.cb_hora.set("antes_16")

        ttk.Label(left, text="Urgente").grid(row=4, column=0, sticky="w", padx=6, pady=6)
        self.cb_urg = ttk.Combobox(left, values=["si", "no"], state="readonly", width=18)
        self.cb_urg.grid(row=4, column=1, padx=6, pady=6)
        self.cb_urg.set("no")

        # Buttons
        btns = ttk.Frame(left)
        btns.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btns, text="Calcular", command=self.run_entrega).pack(side="left", padx=6)
        ttk.Button(btns, text="Cargar ejemplo (Captura A)",
                   command=self.load_example_entrega_a).pack(side="left", padx=6)
        ttk.Button(btns, text="Cargar ejemplo (Captura B)",
                   command=self.load_example_entrega_b).pack(side="left", padx=6)

        # Output
        right = ttk.LabelFrame(frm, text="Resultado")
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.txt_entrega = tk.Text(right, wrap="word", height=30)
        self.txt_entrega.pack(fill="both", expand=True, padx=10, pady=10)

    def load_example_entrega_a(self):
        self.e_peso.delete(0, tk.END); self.e_peso.insert(0, "3")
        self.e_monto.delete(0, tk.END); self.e_monto.insert(0, "180000")
        self.cb_zona.set("centro")
        self.cb_hora.set("antes_16")
        self.cb_urg.set("si")

    def load_example_entrega_b(self):
        self.e_peso.delete(0, tk.END); self.e_peso.insert(0, "30")
        self.e_monto.delete(0, tk.END); self.e_monto.insert(0, "50000")
        self.cb_zona.set("fuera_centro")
        self.cb_hora.set("despues_16")
        self.cb_urg.set("no")

    def run_entrega(self):
        try:
            peso = float(self.e_peso.get().strip())
            monto = float(self.e_monto.get().strip())
            zona = self.cb_zona.get().strip()
            hora = self.cb_hora.get().strip()
            urgente = self.cb_urg.get().strip()
        except Exception:
            messagebox.showerror("Error", "Revisá peso/monto (deben ser numéricos).")
            return

        q = (
            f"plan_entrega({peso}, {monto}, {zona}, {hora}, {urgente}, "
            f"VB, VF, Val, Pri, Plazo, Exp)"
        )

        try:
            r = query_one(self.prolog, q)
        except Exception as e:
            messagebox.showerror("Error Prolog", str(e))
            return

        self.txt_entrega.delete("1.0", tk.END)
        if not r:
            self.txt_entrega.insert(tk.END, "No se pudo inferir. Revisá valores/átomos.\n")
            return

        out = (
            "=== RESULTADO (Entrega) ===\n"
            f"Vehículo base : {fmt_value(r['VB'])}\n"
            f"Vehículo final: {fmt_value(r['VF'])}\n"
            f"Valor         : {fmt_value(r['Val'])}\n"
            f"Prioridad     : {fmt_value(r['Pri'])}\n"
            f"Plazo         : {fmt_value(r['Plazo'])}\n\n"
            "=== EXPLICACIÓN ===\n"
            f"{fmt_exp(r['Exp'])}\n"
        )
        self.txt_entrega.insert(tk.END, out)

    # -------------------------
    # TSP Tab
    # -------------------------
    def _build_tsp_tab(self):
        frm = ttk.Frame(self.tab_tsp)
        frm.pack(fill="both", expand=True)

        left = ttk.LabelFrame(frm, text="Lugares (una línea por lugar: Nombre x y)")
        left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.txt_places = tk.Text(left, wrap="none", height=22)
        self.txt_places.pack(fill="both", expand=True, padx=10, pady=10)

        controls = ttk.Frame(left)
        controls.pack(fill="x", padx=10, pady=10)

        ttk.Label(controls, text="Inicio").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.e_start = ttk.Entry(controls, width=20)
        self.e_start.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(controls, text="Preferencia").grid(row=0, column=2, sticky="w", padx=6, pady=6)
        self.cb_pref = ttk.Combobox(controls, values=["optimo", "rapido"], state="readonly", width=18)
        self.cb_pref.grid(row=0, column=3, padx=6, pady=6)
        self.cb_pref.set("optimo")

        btn_row = ttk.Frame(controls)
        btn_row.grid(row=1, column=0, columnspan=4, pady=10, sticky="w")

        ttk.Button(btn_row, text="Resolver TSP", command=self.run_tsp).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Ejemplo exacto (Captura C)", command=self.load_example_tsp_exacto).pack(side="left", padx=6)
        ttk.Button(btn_row, text="Ejemplo heurístico (Captura D)", command=self.load_example_tsp_heur).pack(side="left", padx=6)

        right = ttk.LabelFrame(frm, text="Resultado")
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.txt_tsp = tk.Text(right, wrap="word", height=30)
        self.txt_tsp.pack(fill="both", expand=True, padx=10, pady=10)

    def load_example_tsp_exacto(self):
        example = "\n".join([
            "A 0 0",
            "B 2 0",
            "C 2 2",
            "D 0 2",
            "E 1 3",
            "F 3 1",
        ])
        self.txt_places.delete("1.0", tk.END)
        self.txt_places.insert(tk.END, example)
        self.e_start.delete(0, tk.END)
        self.e_start.insert(0, "A")
        self.cb_pref.set("optimo")

    def load_example_tsp_heur(self):
        example = "\n".join([
            "A 0 0",
            "B 1 0",
            "C 2 0",
            "D 3 0",
            "E 0 1",
            "F 1 1",
            "G 2 1",
            "H 3 1",
            "I 0 2",
            "J 1 2",
            "K 2 2",
            "L 3 2",
        ])
        self.txt_places.delete("1.0", tk.END)
        self.txt_places.insert(tk.END, example)
        self.e_start.delete(0, tk.END)
        self.e_start.insert(0, "A")
        self.cb_pref.set("optimo")

    def run_tsp(self):
        raw = self.txt_places.get("1.0", tk.END).strip()
        if not raw:
            messagebox.showerror("Error", "Cargá al menos un lugar.")
            return

        coords = {}
        nodes = []

        try:
            for line in raw.splitlines():
                parts = line.strip().split()
                if len(parts) < 3:
                    raise ValueError(f"Línea inválida: {line}")
                name = " ".join(parts[:-2])
                x = float(parts[-2])
                y = float(parts[-1])
                atom = to_atom(name)
                coords[atom] = (x, y)
                nodes.append(atom)
        except Exception as e:
            messagebox.showerror("Error", f"Formato inválido en lugares:\n{e}")
            return

        start_raw = self.e_start.get().strip()
        if not start_raw:
            messagebox.showerror("Error", "Ingresá un inicio.")
            return
        start = to_atom(start_raw)

        if start not in coords:
            messagebox.showerror("Error", "El inicio no coincide con un lugar cargado.")
            return

        pref = self.cb_pref.get().strip()

        try:
            assert_distances(self.prolog, coords)
            nodes_list = "[" + ",".join(nodes) + "]"
            q = f"resolver_tsp({nodes_list}, {start}, {pref}, Ruta, Costo, Metodo, Exp)"
            r = query_one(self.prolog, q)
        except Exception as e:
            messagebox.showerror("Error Prolog", str(e))
            return

        self.txt_tsp.delete("1.0", tk.END)
        if not r:
            self.txt_tsp.insert(tk.END, "No se pudo resolver TSP.\n")
            return

        out = (
            "=== RESULTADO (TSP) ===\n"
            f"Método: {fmt_value(r['Metodo'])}\n"
            f"Costo : {fmt_value(r['Costo'])} (incluye regreso al inicio)\n"
            f"Ruta  : {fmt_value(r['Ruta'])}\n\n"
            "=== EXPLICACIÓN ===\n"
            f"{fmt_exp(r['Exp'])}\n"
        )
        self.txt_tsp.insert(tk.END, out)

def main():
    root = tk.Tk()
    # Mejor look en Windows
    try:
        style = ttk.Style()
        style.theme_use("clam")
    except Exception:
        pass

    ExpertBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
