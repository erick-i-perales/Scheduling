from datetime import datetime, timedelta
from Buffer import Buffer
from Demanda import Demanda
from Maquina import Maquina
from Proceso import Proceso
from Producto import Producto
from Setup import Setup

def manual_schedule(schedule, demanda, start_date, machine, limit_date):
    Procesos = {'Mezclar', 'Hornear', 'Empaquetar'}
    # Check if the machine can handle the product process
    if machine.proceso not in Procesos:
        return False, "Machine cannot handle the specified process"

    # Check if the start date is valid (not before the limit date)
    if start_date < limit_date:
        return False, "Start date is before the limit date"

    # Check the machine's next available time
    machine_next_available = max([entry.end_date for entry in schedule if entry['Machine'] == machine], default=start_date)

    if machine_next_available > start_date:
        return False, "Machine is not available at the specified start date"

    # Calculate the process time
    eficiencia = machine.eficiencia
    process_time = timedelta(minutes=eficiencia)
    end_date = start_date + process_time

    # Add the scheduled job to the schedule
    schedule.append({
        'Producto': demanda.producto,
        'Machine': machine,
        'Start Date': start_date,
        'End Date': end_date,
        'Cantidad': demanda.cantidad
    })

    return True, schedule