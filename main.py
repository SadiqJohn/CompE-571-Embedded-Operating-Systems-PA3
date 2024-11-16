import sys
from EDF import schedule_edf
from RM import schedule_rm
from EE import schedule_ee

def parse_input(file_name):
    """
    Parses the input file to extract system parameters and task descriptions.
    """
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Parse the first line for system parameters
    header = list(map(int, lines[0].strip().split()))
    num_tasks = header[0]
    max_time = header[1]
    power_settings = header[2:]  # Power levels for active and idle states

    # Parse the subsequent lines for task details
    tasks = []
    for line in lines[1:]:
        parts = line.strip().split()
        task = {
            'name': parts[0],
            'period': int(parts[1]),  # Deadline/period of the task
            'wcet': [int(parts[i]) for i in range(2, len(parts))]  # WCETs at different frequencies
        }
        tasks.append(task)

    return num_tasks, max_time, power_settings, tasks

def write_output(schedule, total_energy, output_file):
    """
    Writes the scheduling results and energy consumption to an output file.
    Consecutive IDLE entries are condensed into a single line.
    Ensures fields are aligned for better readability.
    """
    with open(output_file, 'w') as file:
        current_time = 0
        idle_start = None  # Start time of an idle period
        idle_duration = 0
        idle_energy = 0

        # Header for the output
        file.write(f"{'Start':<6} {'Task':<6} {'Freq':<6} {'Dur':<6} {'Energy':<10}\n")
        file.write("=" * 40 + "\n")

        for entry in schedule:
            start_time = current_time
            task_name = entry[1]
            frequency = entry[2]
            duration = entry[3]
            energy = entry[4]

            if task_name == "IDLE":
                # Accumulate idle time and energy
                if idle_start is None:
                    idle_start = start_time
                idle_duration += duration
                idle_energy += energy
            else:
                # Write any accumulated IDLE entries
                if idle_start is not None:
                    file.write(
                        f"{idle_start:<6} {'IDLE':<6} {'IDLE':<6} {idle_duration:<6} {idle_energy:<10.3f}J\n"
                    )
                    idle_start = None
                    idle_duration = 0
                    idle_energy = 0

                # Write the current task entry
                file.write(
                    f"{start_time:<6} {task_name:<6} {frequency:<6} {duration:<6} {energy:<10.3f}J\n"
                )

            current_time += duration

        # Write any remaining IDLE entries
        if idle_start is not None:
            file.write(
                f"{idle_start:<6} {'IDLE':<6} {'IDLE':<6} {idle_duration:<6} {idle_energy:<10.3f}J\n"
            )

        # Write summary statistics
        file.write("=" * 40 + "\n")
        file.write(f"Total Energy: {total_energy:.3f}J\n")
        file.write(f"Total Time: {current_time}\n")

def main():
    """
    Main function to execute the scheduling algorithms based on command-line arguments.
    """
    # Read arguments
    input_file = sys.argv[1]
    strategy = sys.argv[2]
    energy_efficient = len(sys.argv) > 3 and sys.argv[3] == "EE"

    # Parse the input file
    num_tasks, max_time, power_settings, tasks = parse_input(input_file)

    # Select and run the appropriate scheduling algorithm
    if strategy == "EDF" and not energy_efficient:
        schedule, total_energy = schedule_edf(tasks, max_time, power_settings)
    elif strategy == "RM" and not energy_efficient:
        schedule, total_energy = schedule_rm(tasks, max_time, power_settings)
    elif energy_efficient:
        schedule, total_energy = schedule_ee(tasks, max_time, power_settings, strategy)

    # Write the results to an output file
    output_file = f"output_{strategy}{'_EE' if energy_efficient else ''}.txt"
    write_output(schedule, total_energy, output_file)
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    main()
