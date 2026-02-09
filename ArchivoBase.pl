% Vamos a definir una base de conocimiento para clasificar las encomiendas y sus tiempos aproximados de entrega, 
% basándonos en el tipo de vehículo (Con su tiempo base promedio), rangos de peso y el valor de la encomienda.

% ===============================
% TIPOS DE VEHICULOS (segun capacidad de carga)
% ===============================

vehiculo(moto).
vehiculo(camioneta).
vehiculo(camion).

% ===============================
% RANGOS DE PESO (en kg)
% ===============================

vehiculo_por_peso(Peso, moto) :-
    Peso =< 5.

vehiculo_por_peso(Peso, camioneta) :-
    Peso > 5,
    Peso =< 40.

vehiculo_por_peso(Peso, camion) :-
    Peso > 40.

% ===============================
% CLASIFICACION POR VALOR DEL PRODUCTO  
% ===============================

valor(alto).
valor(medio).
valor(bajo).

clasificar_valor(Monto, alto) :-
    Monto >= 150000.

clasificar_valor(Monto, medio) :-
    Monto >= 20000,
    Monto < 150000.

clasificar_valor(Monto, bajo) :-
    Monto < 20000.

% ===============================
% TIEMPO BASE SEGUN VEHICULO
% (en horas aproximadas)
% ===============================

tiempo_base(moto, 24).
tiempo_base(camioneta, 48).
tiempo_base(camion, 120).
