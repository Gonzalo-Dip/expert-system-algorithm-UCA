% tsp.pl
:- dynamic dist/3.

% ---------------------------------------
% Utilidades
% ---------------------------------------

% Asegura que exista dist en ambos sentidos (si solo cargaste uno)
dist_sym(A,B,D) :- dist(A,B,D), !.
dist_sym(A,B,D) :- dist(B,A,D).

path_cost([_], 0).
path_cost([A,B|Rest], Cost) :-
    dist_sym(A,B,D),
    path_cost([B|Rest], CostRest),
    Cost is D + CostRest.

% ---------------------------------------
% TSP exacto (para N chico)
% Devuelve Ruta = [Start, ..., Last] y el costo incluye volver a Start
% ---------------------------------------
tsp_exacto(Nodes, Start, Ruta, Costo) :-
    select(Start, Nodes, Rest),
    findall(Cost-Path,
        (
            permutation(Rest, Perm),
            Path = [Start|Perm],
            append(Path, [Start], Cycle),
            path_cost(Cycle, Cost)
        ),
        Solutions),
    sort(Solutions, [Costo-Ruta|_]).

% ---------------------------------------
% TSP heurístico: Nearest Neighbor (greedy)
% ---------------------------------------
tsp_nn(Nodes, Start, Ruta, Costo) :-
    select(Start, Nodes, Unvisited0),
    nn_build(Start, Unvisited0, [Start], Ruta),
    append(Ruta, [Start], Cycle),
    path_cost(Cycle, Costo).

nn_build(_Current, [], AccRev, Ruta) :-
    reverse(AccRev, Ruta).
nn_build(Current, Unvisited, AccRev, Ruta) :-
    % Elegir el más cercano
    setof(D-Next,
          (member(Next, Unvisited), dist_sym(Current, Next, D)),
          [ _MinD-Choice | _ ]),
    select(Choice, Unvisited, Unvisited2),
    nn_build(Choice, Unvisited2, [Choice|AccRev], Ruta).
