#FIRMATLOG 🏅


El proyecto implementa un sistema experto orientado a la logística de distribución, capaz de tomar decisiones mediante reglas de inferencia. Su función es asistir al cliente y a la empresa en la estimación del tiempo de entrega, aplicando conocimiento formalizado sobre peso, valor del pedido y recursos de transporte, simulando el razonamiento de un operador con experiencia.



<img width="500" height="400" src="https://github.com/user-attachments/assets/2847ae2b-0b0d-4e53-9c3f-ecf0819b9530" />



## 📌 Parámetros utilizados por el sistema

**Peso del pedido (kg)**
Determina el tipo de vehículo necesario para el transporte.

**Monto del pedido ($)**
Se utiliza para clasificar el valor en alto, medio o bajo y definir la prioridad.

**Hora de carga**
Diferencia si el pedido se registró antes o después de las 16:00.

**Zona de entrega**
Indica si el destino se encuentra en el centro de la ciudad o fuera del área cercana.

**Urgencia del cliente**
Permite aumentar la prioridad del envío si el pedido requiere tratamiento especial.

**Vehículo asignado**
Resultado de la inferencia: moto, camioneta o camión.

**Prioridad final**
Nivel calculado según valor y urgencia: baja, media, alta o máxima.

**Tiempo estimado de entrega**
Plazo final inferido por el sistema experto.
