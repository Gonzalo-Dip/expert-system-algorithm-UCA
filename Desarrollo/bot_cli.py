from pyswip import Prolog
from pathlib import Path
import math

def to_atom(name: str) -> str:
    # convierte "Casa Central" -> casa_central (átomo Prolog)
    s = name.strip().lower().replace(" ", "_")
    s = "".join(ch for ch in s if ch.isalnum() or ch == "_")
    if not s:
        raise ValueError("Nombre inválido")
    return s

def euclid(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def assert_distances(prolog: Prolog, coords: dict):
    # limpiar dist/3 previas
    list(prolog.query("retractall(dist(_,_,_))"))

    nodes = list(coords.keys())
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            a, b = nodes[i], nodes[j]
            d = euclid(coords[a], coords[b])
            # asertamos ambos sentidos (más simple)
            prolog.assertz(f"dist({a},{b},{d})")
            prolog.assertz(f"dist({b},{a},{d})")

def query_one(prolog: Prolog, q: str):
    res = list(prolog.query(q))
    return res[0] if res else None

def modo_entrega(prolog: Prolog):
    peso = float(input("Peso (kg): ").strip())
    monto = float(input("Monto ($): ").strip())
    zona = input("Zona (centro / fuera_centro): ").strip()
    hora = input("Hora (antes_16 / despues_16): ").strip()
    urgente = input("Urgente (si / no): ").strip()

    q = (
        f"plan_entrega({peso}, {monto}, {zona}, {hora}, {urgente}, "
        f"VB, VF, Val, Pri, Plazo, Exp)"
    )
    r = query_one(prolog, q)
    if not r:
        print("No se pudo inferir (revisá datos/átomos).")
        return

    print("\n=== RESULTADO ===")
    print("Vehículo base:", r["VB"])
    print("Vehículo final:", r["VF"])
    print("Valor:", r["Val"])
    print("Prioridad:", r["Pri"])
    print("Plazo:", r["Plazo"])
    print("Explicación:", r["Exp"])
    print()

def modo_tsp(prolog: Prolog):
    n = int(input("Cantidad de lugares: ").strip())
    coords = {}
    nodes = []

    print("Ingresá nombre + coordenadas (x y). Ej: 'Deposito' 10 5")
    for _ in range(n):
        parts = input("Lugar: ").strip().split()
        name = " ".join(parts[:-2])
        x = float(parts[-2])
        y = float(parts[-1])
        atom = to_atom(name)
        coords[atom] = (x, y)
        nodes.append(atom)

    start = to_atom(input("Inicio (nombre igual a uno de los lugares): ").strip())
    pref = input("Preferencia (optimo / rapido): ").strip()

    if start not in coords:
        print("El inicio no coincide con un lugar cargado.")
        return

    assert_distances(prolog, coords)

    # lista Prolog: [a,b,c]
    nodes_list = "[" + ",".join(nodes) + "]"
    q = f"resolver_tsp({nodes_list}, {start}, {pref}, Ruta, Costo, Metodo, Exp)"
    r = query_one(prolog, q)

    if not r:
        print("No se pudo resolver TSP (revisá distancias/entrada).")
        return

    print("\n=== RUTA TSP ===")
    print("Método:", r["Metodo"])
    print("Costo (incluye regreso):", r["Costo"])
    print("Ruta:", r["Ruta"])
    print("Explicación:", r["Exp"])
    print()

def main():
    prolog = Prolog()

    # Cargar route_motor.pl (que a su vez carga motor.pl + tsp.pl)
    base_dir = Path(__file__).resolve().parent  # Desarrollo/
    route_motor = base_dir / "route_motor.pl"
    prolog.consult(str(route_motor))

    while True:
        print("1) Evaluar una entrega (plan_entrega)")
        print("2) Ruta TSP (NP - viajante)")
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            modo_entrega(prolog)
        elif op == "2":
            modo_tsp(prolog)
        elif op == "0":
            break
        else:
            print("Opción inválida.\n")

if __name__ == "__main__":
    main()
