def manual_unschedule(schedule, producto, cantidad, start_date, machine):
    # Find the job to be unscheduled
    job_to_unschedule = None
    for entry in schedule:
        if (entry['Producto'] == producto and 
            entry['Cantidad'] == cantidad and 
            entry['Start Date'] == start_date and 
            entry['Machine'] == machine):
            job_to_unschedule = entry
            break

    if job_to_unschedule:
        schedule.remove(job_to_unschedule)
        return True, schedule
    else:
        return False, "Job not found in the schedule"