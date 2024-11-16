from EDF import schedule_edf
from RM import schedule_rm

def calculate_energy(wcet, power):
    """
    Calculates energy consumption using:
    Energy (J) = (WCET (s) * Power (mW)) / 1000
    """
    return (wcet * power) / 1000

def find_best_frequency(task, time, power_settings, current_time):
    """
    Finds the lowest feasible frequency for a task while minimizing energy.
    Ensures the task meets its deadline and avoids unnecessary idle periods.
    """
    frequencies = [1188, 918, 648, 384]  # CPU frequencies in MHz
    best_freq = None
    best_wcet = None
    best_energy = float('inf')

    for freq_index in range(len(frequencies)):
        wcet = task['wcet'][freq_index]
        if current_time + wcet <= time + task['period']:  # Meets deadline
            energy = calculate_energy(wcet, power_settings[freq_index])
            if energy < best_energy:
                best_freq = frequencies[freq_index]
                best_wcet = wcet
                best_energy = energy

    return best_freq, best_wcet, best_energy

def schedule_ee(tasks, max_time, power_settings, strategy):
    """
    Schedules tasks using energy-efficient EDF or RM algorithms.
    Dynamically optimizes frequency and minimizes idle periods.
    """
    time = 0
    schedule = []
    total_energy = 0

    # Select the scheduling logic based on the strategy
    if strategy == "EDF":
        scheduler = schedule_edf
    elif strategy == "RM":
        scheduler = schedule_rm
    else:
        raise ValueError("Invalid strategy. Use 'EDF' or 'RM'.")

    while time < max_time:
        ready_tasks = [task for task in tasks if time % task['period'] == 0]

        if ready_tasks:
            # Use the selected scheduler to find the next task
            if strategy == "EDF":
                # EDF: Task with earliest deadline
                selected_task = None
                for task in ready_tasks:
                    if selected_task is None or (time + task['period']) < (time + selected_task['period']):
                        selected_task = task
            else:
                # RM: Task with shortest period
                selected_task = None
                for task in ready_tasks:
                    if selected_task is None or task['period'] < selected_task['period']:
                        selected_task = task

            # Optimize the task's frequency and energy
            freq, wcet, energy = find_best_frequency(selected_task, time, power_settings, time)
            if freq is not None:
                schedule.append((time, selected_task['name'], freq, wcet, energy))
                time += wcet
                total_energy += energy
            else:
                # No feasible frequency; this should not happen
                raise ValueError(f"Task {selected_task['name']} cannot meet its deadline.")
        else:
            # No tasks ready; idle the CPU
            idle_energy = calculate_energy(1, power_settings[-1])  # Idle power
            schedule.append((time, "IDLE", "IDLE", 1, idle_energy))
            time += 1
            total_energy += idle_energy

    return schedule, total_energy
