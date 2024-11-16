def calculate_energy(wcet, power):
    """
    Calculates energy consumption using:
    Energy (J) = (WCET (s) * Power (mW)) / 1000
    """
    return (wcet * power) / 1000

def schedule_edf(tasks, max_time, power_settings):
    """
    Schedules tasks using Earliest Deadline First (EDF) algorithm.
    Selects the task with the closest absolute deadline at each time step.
    """
    time = 0
    schedule = []
    total_energy = 0

    while time < max_time:
        ready_tasks = []
        for task in tasks:
            # Check if the task is ready to run
            if time % task['period'] == 0:
                ready_tasks.append(task)

        if ready_tasks:
            # Find the task with the nearest absolute deadline
            earliest_deadline_task = None
            for task in ready_tasks:
                if (earliest_deadline_task is None or
                        (time + task['period']) < (time + earliest_deadline_task['period'])):
                    earliest_deadline_task = task

            # Schedule the selected task
            wcet = earliest_deadline_task['wcet'][0]  # Use WCET at max frequency
            energy = calculate_energy(wcet, power_settings[0])  # Max power
            schedule.append((time, earliest_deadline_task['name'], 1188, wcet, energy))
            time += wcet
            total_energy += energy
        else:
            # If no task is ready, the CPU is idle
            idle_energy = calculate_energy(1, power_settings[-1])  # Idle power
            schedule.append((time, "IDLE", "IDLE", 1, idle_energy))
            time += 1
            total_energy += idle_energy

    return schedule, total_energy
