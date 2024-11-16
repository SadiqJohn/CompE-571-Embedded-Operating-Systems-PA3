def calculate_energy(wcet, power):
    """
    Calculates energy consumption using:
    Energy (J) = (WCET (s) * Power (mW)) / 1000
    """
    return (wcet * power) / 1000

def schedule_rm(tasks, max_time, power_settings):
    """
    Schedules tasks using Rate Monotonic (RM) algorithm.
    Fixed priority: shorter period = higher priority.
    """
    # Sort tasks by their periods (shortest period = highest priority)
    sorted_tasks = []
    for task in tasks:
        inserted = False
        for i in range(len(sorted_tasks)):
            if task['period'] < sorted_tasks[i]['period']:
                sorted_tasks.insert(i, task)
                inserted = True
                break
        if not inserted:
            sorted_tasks.append(task)

    time = 0
    schedule = []
    total_energy = 0

    while time < max_time:
        scheduled = False
        for task in sorted_tasks:
            # Check if the task is ready to run
            if time % task['period'] == 0:
                wcet = task['wcet'][0]  # Use WCET at max frequency
                energy = calculate_energy(wcet, power_settings[0])  # Max power
                schedule.append((time, task['name'], 1188, wcet, energy))
                time += wcet
                total_energy += energy
                scheduled = True
                break  # Only one task can run at a time

        if not scheduled:
            # If no task is ready, the CPU is idle
            idle_energy = calculate_energy(1, power_settings[-1])  # Idle power
            schedule.append((time, "IDLE", "IDLE", 1, idle_energy))
            time += 1
            total_energy += idle_energy

    return schedule, total_energy
