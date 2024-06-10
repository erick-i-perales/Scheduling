from Buffer import Buffer
from Demanda import Demanda
from Maquina import Maquina
from Proceso import Proceso
from Producto import Producto
from Setup import Setup
from datetime import datetime, timedelta

def automatic_schedule(demandas, productos, maquinas, setups, buffers):
    # Sort demand by fecha_limite
    sorted_demandas = sorted(demandas, key=lambda x: x.fecha_limite)
    # Initialize today's date with time set to 00:00:00
    today = datetime.combine(datetime.today(), datetime.min.time())
    # Initialize scheduling variables
    schedule = []
    machine_times = {maquina.id_maquina: today for maquina in maquinas}
    last_product = {maquina.id_maquina: None for maquina in maquinas}
    mixed_dough = 0
    # Schedule the 'Mezclar' process
    for demanda in sorted_demandas:
        producto = next(prod for prod in productos if prod.id_producto == demanda.producto)
        cantidad = demanda.cantidad

        while cantidad > 0:
            # Find the earliest available 'Mezclar' machine
            machine = min(maquinas, key=lambda m: machine_times[m.id_maquina])
            start_time = machine_times[machine.id_maquina]

            # Check for setup time
            if last_product[machine.id_maquina] and last_product[machine.id_maquina] != producto.id_producto:
                setup = next(setup for setup in setups if setup.producto_previo == last_product[machine.id_maquina] and setup.producto_posterior == producto.id_producto and setup.proceso == 'Mezclar')
                setup_time = timedelta(minutes=setup.setup)
                start_time += setup_time

            # Calculate the process time
            eficiencia = machine.eficiencia
            process_time = timedelta(minutes=eficiencia)
            end_time = start_time + process_time

            # Update the schedule
            process_quantity = min(cantidad, machine.salida)
            schedule.append({'Producto': producto.nombre,'Machine': machine.id_maquina,'Start Date': start_time,'End Date': end_time,'Cantidad': process_quantity})

            # Update the machine's next available time and the last processed product
            machine_times[machine.id_maquina] = end_time
            last_product[machine.id_maquina] = producto.id_producto

            # Update the mixed dough and remaining quantity
            mixed_dough += process_quantity
            cantidad -= process_quantity

            # Check if we have enough mixed dough to start 'Hornear'
            if mixed_dough >= next(maquina.entrada for maquina in maquinas if maquina.proceso == 'Hornear'):
                horno = next(maquina for maquina in maquinas if maquina.proceso == 'Hornear')
                horno_start_time = max(machine_times[horno.id_maquina], end_time) + timedelta(minutes=next(buffer.tiempo for buffer in buffers if buffer.proceso_anterior == 'Mezclar' and buffer.proceso_siguiente == 'Hornear'))
                horno_process_time = timedelta(minutes=horno.eficiencia)
                horno_end_time = horno_start_time + horno_process_time

                schedule.append({'Producto': producto.nombre,'Machine': horno.id_maquina,'Start Date': horno_start_time,'End Date': horno_end_time,'Cantidad': horno.salida})

                machine_times[horno.id_maquina] = horno_end_time
                mixed_dough -= horno.salida

                # Schedule 'Empaquetar' process for the units
                empaquetar_quantity = horno.salida
                empaquetar_machines = [maquina for maquina in maquinas if maquina.proceso == 'Empaquetar']
                for empaquetar_machine in empaquetar_machines:
                    if empaquetar_quantity <= 0:
                        break
                    empaquetar_process_quantity = min(empaquetar_quantity, empaquetar_machine.entrada)
                    empaquetar_start_time = max(machine_times[empaquetar_machine.id_maquina], horno_end_time) + timedelta(minutes=next(buffer.tiempo for buffer in buffers if buffer.proceso_anterior == 'Hornear' and buffer.proceso_siguiente == 'Empaquetar'))
                    empaquetar_process_time = timedelta(minutes=empaquetar_machine.eficiencia)
                    empaquetar_end_time = empaquetar_start_time + empaquetar_process_time

                    schedule.append({'Producto': producto.nombre,'Machine': empaquetar_machine.id_maquina,'Start Date': empaquetar_start_time,'End Date': empaquetar_end_time,'Cantidad': empaquetar_process_quantity})

                    machine_times[empaquetar_machine.id_maquina] = empaquetar_end_time
                    empaquetar_quantity -= empaquetar_process_quantity
    return schedule