
import sys
from EDF import schedule_edf
from RM import schedule_rm

def parse_input(file_name):
    """Parses the input file to extract tasks and system parameters."""
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Extract system parameters from the first line
    header = list(map(int, lines[0].strip().split()))
    max_time = header[1]
    power_settings = header[2:]

    # Extract task details
    tasks = []
    for line in lines[1:]:
        parts = line.strip().split()
        task = {
            "name": parts[0],
            "deadline": int(parts[1]),
            "wcet": list(map(int, parts[2:]))
        }
        tasks.append(task)

    return tasks, max_time, power_settings

def print_schedule(schedule, total_energy, idle_time, total_time):
    """Prints the schedule and additional information."""
    print("-------------------------------------------")
    print(f"        Printing Schedule Process")
    print("-------------------------------------------")
    print("<Time Started>  <Task Name>     <CPU Freq>      <Runtime>       <NRG Consumed>")
    for entry in schedule:
        print(f"{entry[0]:<16}  {entry[1]:<12}  {entry[2]:<12}  {entry[3]:<12}  {entry[4]:.2f} J")

    idle_rate = (idle_time / total_time) * 100
    print("-------------------------------------------")
    print(f"        Additional Information")
    print("-------------------------------------------")
    print(f"Total Energy Consumption: {total_energy:.2f}J      Idle Rate: {idle_rate:.1f}%         Total Execution Time: {total_time}s")

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <input_file> <EDF|RM>")
        sys.exit(1)

    input_file = sys.argv[1]
    algorithm = sys.argv[2].upper()

    tasks, max_time, power_settings = parse_input(input_file)

    if algorithm == "EDF":
        print("-------------------------------------------")
        print(f"        Now running EDF")
        print("-------------------------------------------")
        schedule, total_energy, idle_time, total_time = schedule_edf(tasks, max_time, power_settings)
    elif algorithm == "RM":
        print("-------------------------------------------")
        print(f"        Now running RM")
        print("-------------------------------------------")
        schedule, total_energy, idle_time, total_time = schedule_rm(tasks, max_time, power_settings)
    else:
        print("Invalid algorithm. Choose EDF or RM.")
        sys.exit(1)

    print_schedule(schedule, total_energy, idle_time, total_time)

if __name__ == "__main__":
    main()
