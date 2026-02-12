from pyswip import Prolog

prolog = Prolog()

# Cargá el motor (esto a su vez consultará ajustes_de_logica.pl)
prolog.consult("Desarrollo/motor.pl")

res = list(prolog.query("plan_entrega(50, 180000, centro, antes_16, si, VB, VF, Val, Pri, Plazo, Exp)"))
if not res:
    print("No hay solución para esos parámetros")
else:
    print(res[0])

#for r in prolog.query("plan_entrega(10, 50000, fuera_centro, antes_16, no, VB, VF, Val, Pri, Plazo, Exp)"):
#    print(r)

r = res[0]
print("VehBase:", r["VB"])
print("VehFinal:", r["VF"])
print("Valor:", r["Val"])
print("Prioridad:", r["Pri"])
print("Plazo:", r["Plazo"])
print("Explicación:")
for item in r["Exp"]:
    print(" -", item)


def plan_entrega(prolog, peso, monto, zona, hora, urgente):
    q = f"plan_entrega({peso}, {monto}, {zona}, {hora}, {urgente}, VB, VF, Val, Pri, Plazo, Exp)"
    res = list(prolog.query(q))
    return res[0] if res else None
