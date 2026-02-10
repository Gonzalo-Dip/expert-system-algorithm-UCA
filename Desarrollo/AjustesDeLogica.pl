% ===============================
% AJUSTE DE VEHICULO POR ZONA
% ===============================

vehiculo_ajustado(moto, fuera_centro, camioneta).
vehiculo_ajustado(V, centro, V).
vehiculo_ajustado(camioneta, fuera_centro, camioneta).
vehiculo_ajustado(camion, _, camion).

% ===============================
% PRIORIDAD SEGUN VALOR
% ===============================

prioridad(alto, alta).
prioridad(medio, media).
prioridad(bajo, baja).



% ===============================
% AJUSTE POR URGENCIA DEL CLIENTE
% ===============================

ajustar_prioridad(alta, si, maxima).
ajustar_prioridad(media, si, alta).
ajustar_prioridad(baja, si, media).
ajustar_prioridad(P, no, P).



% ===============================
% TIEMPO SEGUN HORA DE CARGA Y VEHICULO (AJUSTE DE HORARIO)
% ===============================

ajuste_horario(moto, antes_16, mismo_dia).
ajuste_horario(moto, despues_16, dia_siguiente).

ajuste_horario(camioneta, _, uno_a_dos_dias).
ajuste_horario(camion, _, dentro_semana).

% ===============================
% REDUCCION DE TIEMPO POR PRIORIDAD
% ===============================

reducir_tiempo(mismo_dia, maxima, inmediato).
reducir_tiempo(dia_siguiente, maxima, mismo_dia).
reducir_tiempo(T, _, T).