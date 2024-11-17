
def calculate_energy(wcet, power):
    """Calculates energy consumption for a task based on WCET and power."""
    return wcet * power / 1000

def schedule_rm(tasks, max_time, power_settings):
    """Schedules tasks using the RM algorithm."""
    time = 0
    schedule = []
    total_energy = 0
    idle_time = 0

    # Sort tasks by their period (or deadline, in this case)
    tasks.sort(key=lambda t: t["deadline"])

    while time < max_time:
        # Find tasks ready to execute
        ready_tasks = [task for task in tasks if task["deadline"] >= time]
        if ready_tasks:
            # Select the task with the shortest period (highest priority)
            task = ready_tasks[0]
            wcet = task["wcet"][0]
            power = power_settings[0]
            schedule.append((time, task["name"], 1188, wcet, calculate_energy(wcet, power)))
            time += wcet
            total_energy += calculate_energy(wcet, power)
        else:
            # If no task is ready, the system is idle
            idle_duration = 15
            schedule.append((time, "IDLE", "IDLE", idle_duration, calculate_energy(idle_duration, power_settings[-1])))
            idle_time += idle_duration
            time += idle_duration
            total_energy += calculate_energy(idle_duration, power_settings[-1])

    return schedule, total_energy, idle_time, time
