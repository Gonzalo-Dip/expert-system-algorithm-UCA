:- consult('base.pl').
:- consult('Ajustelogistica.pl').

% -------------------------------
% Validaciones simples
% -------------------------------
zona_valida(centro).
zona_valida(fuera_centro).

hora_valida(antes_16).
hora_valida(despues_16).

si_no(si).
si_no(no).

% -------------------------------
% Regla principal del sistema experto
% plan_entrega(+Peso,+Monto,+Zona,+HoraCarga,+Urgente,
%              -VehiculoBase,-VehiculoFinal,-ValorCat,-PrioridadFinal,-PlazoFinal,-Explicacion)
% -------------------------------

plan_entrega(Peso, Monto, Zona, HoraCarga, Urgente,
            VehBase, VehFinal, ValorCat, PriFinal, PlazoFinal,
            Explicacion) :-

    % Validaciones mínimas
    number(Peso), Peso > 0,
    number(Monto), Monto >= 0,
    zona_valida(Zona),
    hora_valida(HoraCarga),
    si_no(Urgente),

    % 1) Vehículo por peso
    vehiculo_por_peso(Peso, VehBase),

    % 2) Ajuste de vehículo por zona
    (   vehiculo_ajustado(VehBase, Zona, VehFinal)
    ->  true
    ;   VehFinal = VehBase
    ),

    % 3) Valor del producto
    clasificar_valor(Monto, ValorCat),

    % 4) Prioridad por valor + ajuste por urgencia
    prioridad(ValorCat, Pri0),
    ajustar_prioridad(Pri0, Urgente, PriFinal),

    % 5) Plazo por horario + reducción por prioridad
    ajuste_horario(VehFinal, HoraCarga, Plazo0),
    reducir_tiempo(Plazo0, PriFinal, PlazoFinal),

    % 6) Explicación (lista de “razones”)
    Explicacion = [
        razon(vehiculo_por_peso(Peso, VehBase)),
        razon(vehiculo_ajustado(VehBase, Zona, VehFinal)),
        razon(clasificar_valor(Monto, ValorCat)),
        razon(prioridad_por_valor(ValorCat, Pri0)),
        razon(ajuste_por_urgencia(Pri0, Urgente, PriFinal)),
        razon(ajuste_horario(VehFinal, HoraCarga, Plazo0)),
        razon(reducir_tiempo(Plazo0, PriFinal, PlazoFinal))
    ].

% -------------------------------
% (Opcional) Tiempo base numérico (horas) del vehículo final
% -------------------------------
tiempo_estimado(Peso, Monto, Zona, HoraCarga, Urgente, VehFinal, HorasBase) :-
    plan_entrega(Peso, Monto, Zona, HoraCarga, Urgente,
                 _VehBase, VehFinal, _ValorCat, _PriFinal, _PlazoFinal, _Exp),
    tiempo_base(VehFinal, HorasBase).
