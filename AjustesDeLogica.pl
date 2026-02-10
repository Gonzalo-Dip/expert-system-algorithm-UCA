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
