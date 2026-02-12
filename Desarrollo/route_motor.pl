% route_motor.pl

% Cargar motor.pl y tsp.pl desde la misma carpeta de este archivo
:- prolog_load_context(directory, Dir),
   directory_file_path(Dir, 'motor.pl', M),
   directory_file_path(Dir, 'tsp.pl', T),
   ensure_loaded(M),
   ensure_loaded(T).

% ---------------------------------------
% Selector experto del método TSP
% Preferencia: optimo | rapido
% Si N <= 9 y preferencia = optimo => exacto
% Si no => heurístico (NN)
% ---------------------------------------
resolver_tsp(Nodes, Start, Preferencia, Ruta, Costo, Metodo, Explicacion) :-
    length(Nodes, N),
    ( Preferencia = optimo, N =< 9 ->
        Metodo = exacto,
        tsp_exacto(Nodes, Start, Ruta, Costo)
    ;
        Metodo = heuristico_nn,
        tsp_nn(Nodes, Start, Ruta, Costo)
    ),
    Explicacion = [
        paso(n_ciudades, N),
        paso(preferencia, Preferencia),
        paso(metodo, Metodo),
        paso(costo_incluye_regreso_al_inicio, si)
    ].
