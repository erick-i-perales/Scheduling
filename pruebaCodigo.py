from Buffer import Buffer
from Demanda import Demanda
from Maquina import Maquina
from Proceso import Proceso
from Producto import Producto
from Setup import Setup
from datetime import datetime, timedelta
from automatic_schedule import automatic_schedule
from manual_schedule import manual_schedule
from manual_unschedule import manual_unschedule

# Create demand objects
demanda1 = Demanda(id_demanda='D1', nombre='Cliente1', producto='P1', cantidad=150, fecha_limite=datetime.strptime('06/10/24', '%m/%d/%y'))
demanda2 = Demanda(id_demanda='D2', nombre='Cliente1', producto='P2', cantidad=100, fecha_limite=datetime.strptime('06/15/24', '%m/%d/%y'))
demanda3 = Demanda(id_demanda='D3', nombre='Cliente2', producto='P1', cantidad=200, fecha_limite=datetime.strptime('06/10/24', '%m/%d/%y'))
demanda4 = Demanda(id_demanda='D4', nombre='Cliente3', producto='P2', cantidad=50, fecha_limite=datetime.strptime('06/13/24', '%m/%d/%y'))

# Create product objects
producto1 = Producto(id_producto='P1', nombre='Blanco', id_formula='F1', venta=30)
producto2 = Producto(id_producto='P2', nombre='Integral', id_formula='F2', venta=35)

# Create machine objects
maquina1 = Maquina(id_maquina='M1', proceso='Mezclar', eficiencia=15, entrada=30, salida=30)
maquina2 = Maquina(id_maquina='M2', proceso='Mezclar', eficiencia=15, entrada=30, salida=30)
maquina3 = Maquina(id_maquina='H1', proceso='Hornear', eficiencia=60, entrada=120, salida=120)
maquina4 = Maquina(id_maquina='E1', proceso='Empaquetar', eficiencia=5, entrada=30, salida=30)
maquina5 = Maquina(id_maquina='E2', proceso='Empaquetar', eficiencia=5, entrada=30, salida=30)

# Create setup objects
setup1 = Setup(id_setup='S1', producto_previo='P1', producto_posterior='P2', proceso='Mezclar', setup=15)
setup2 = Setup(id_setup='S2', producto_previo='P2', producto_posterior='P1', proceso='Mezclar', setup=15)
setup3 = Setup(id_setup='S3', producto_previo='P1', producto_posterior='P2', proceso='Hornear', setup=20)
setup4 = Setup(id_setup='S4', producto_previo='P2', producto_posterior='P1', proceso='Hornear', setup=20)

# Create buffer objects
buffer1 = Buffer(id_buffer='B1', tiempo=5, proceso_anterior='Mezclar', proceso_siguiente='Hornear')
buffer2 = Buffer(id_buffer='B2', tiempo=10, proceso_anterior='Hornear', proceso_siguiente='Empaquetar')

# Call the function with the created objects
schedule = automatic_schedule([demanda1, demanda2, demanda3, demanda4],
                           [producto1, producto2],
                           [maquina1, maquina2, maquina3, maquina4, maquina5],
                           [setup1, setup2, setup3, setup4],
                           [buffer1, buffer2])

# Output the schedule   
for entry in schedule:
    print(entry)

limit_date = datetime(2024, 6, 8, 0, 0)

# Create instances of Demanda and Maquina classes
demanda = Demanda(id_demanda='D5', nombre='Cliente3', producto='P1', cantidad=200, fecha_limite=datetime(2024, 6, 10, 0, 0))

# Manual scheduling a new job
start_date = datetime(2024, 6, 15, 0, 0)
success, result = manual_schedule(schedule, demanda, start_date, maquina1, limit_date)
if success:
    print("Schedule updated:", result)
else:
    print("Scheduling failed:", result)

# Manual unscheduling a job
start_date = datetime(2024, 6, 15, 0, 0)
producto = 'P1'
cantidad = 200
success, result = manual_unschedule(schedule, producto, cantidad, start_date, maquina1)
if success:
    print("Schedule updated:", result)
else:
    print("Unscheduling failed:", result)