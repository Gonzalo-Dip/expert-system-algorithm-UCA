# Complejidad del sistema

## 1) Motor experto: plan_entrega/11
La inferencia ejecuta una cantidad fija de reglas:
- vehiculo_por_peso/2
- vehiculo_ajustado/3
- clasificar_valor/2
- prioridad/2 y ajustar_prioridad/3
- ajuste_horario/3 y reducir_tiempo/3

No recorre estructuras crecientes (no hay listas grandes ni búsqueda combinatoria).
**Tiempo:** O(1) por consulta (constante).  
**Memoria:** O(1).

## 2) NP: Problema del Viajante (TSP) con selector experto
Se resuelve con dos métodos y el sistema elige según N y preferencia:

### a) Exacto (tsp_exacto/4)
Enumera permutaciones de (N-1) nodos y calcula el costo del tour.
Cantidad de tours ~ (N-1)! y cada costo se calcula en O(N).

**Tiempo:** O(N · (N-1)!) ≈ O(N!)  
**Memoria:** alta si se guardan soluciones; crece con el número de tours evaluados.

### b) Heurístico Nearest Neighbor (tsp_nn/4)
En cada paso elige el vecino más cercano entre los no visitados.
Se repite N veces, buscando un mínimo en una lista decreciente.

**Tiempo:** O(N²)  
**Memoria:** O(N)

## 3) Regla de decisión del sistema experto (método TSP)
- Si preferencia=optimo y N<=9 → método exacto (viable).
- Caso contrario → heurístico NN (evita explosión combinatoria).

Esto justifica la elección automática por complejidad.
