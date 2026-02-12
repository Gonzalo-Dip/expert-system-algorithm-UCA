% motor.pl
:- consult('AjustesDeLogica.pl').

% -------------------------------
% Validaciones mínimas
% -------------------------------
zona_valida(centro).
zona_valida(fuera_centro).

hora_valida(antes_16).
hora_valida(despues_16).

si_no(si).
si_no(no).

% -------------------------------
% Predicado principal del sistema experto
% plan_entrega(+Peso,+Monto,+Zona,+HoraCarga,+Urgente,
%              -VehBase,-VehFinal,-ValorCat,-PriFinal,-PlazoFinal,-Explicacion)
% -------------------------------
plan_entrega(Peso, Monto, Zona, HoraCarga, Urgente,
            VehBase, VehFinal, ValorCat, PriFinal, PlazoFinal, Explicacion) :-

    % Validaciones
    number(Peso), Peso > 0,
    number(Monto), Monto >= 0,
    zona_valida(Zona),
    hora_valida(HoraCarga),
    si_no(Urgente),

    % 1) Vehículo por peso
    vehiculo_por_peso(Peso, VehBase),

    % 2) Ajuste por zona
    (   vehiculo_ajustado(VehBase, Zona, VehFinal)
    ->  true
    ;   VehFinal = VehBase
    ),

    % 3) Clasificación por valor
    clasificar_valor(Monto, ValorCat),

    % 4) Prioridad por valor + urgencia
    prioridad(ValorCat, Pri0),
    ajustar_prioridad(Pri0, Urgente, PriFinal),

    % 5) Plazo por horario + reducción por prioridad
    ajuste_horario(VehFinal, HoraCarga, Plazo0),
    reducir_tiempo(Plazo0, PriFinal, PlazoFinal),

    % 6) Explicación (para mostrar "por qué")
    Explicacion = [
        paso(vehiculo_por_peso, Peso, VehBase),
        paso(vehiculo_ajustado, VehBase, Zona, VehFinal),
        paso(clasificar_valor, Monto, ValorCat),
        paso(prioridad, ValorCat, Pri0),
        paso(ajustar_prioridad, Pri0, Urgente, PriFinal),
        paso(ajuste_horario, VehFinal, HoraCarga, Plazo0),
        paso(reducir_tiempo, Plazo0, PriFinal, PlazoFinal)
    ].

% (Opcional) obtener horas base del vehículo final
tiempo_base_final(Peso, Monto, Zona, HoraCarga, Urgente, VehFinal, HorasBase) :-
    plan_entrega(Peso, Monto, Zona, HoraCarga, Urgente,
                 _VB, VehFinal, _Val, _Pri, _Plazo, _Exp),
    tiempo_base(VehFinal, HorasBase).

% (Opcional) versión corta para el bot
recomendacion(Peso, Monto, Zona, HoraCarga, Urgente, VehFinal, PriFinal, PlazoFinal) :-
    plan_entrega(Peso, Monto, Zona, HoraCarga, Urgente,
                 _VB, VehFinal, _Val, PriFinal, PlazoFinal, _Exp).
