# scheduler.py
import sys
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Task:
    name: str
    period: int
    wcets: List[int]
    deadline: int = 0
    next_release: int = 0
    remaining_time: int = 0
    current_freq_idx: int = 0
    initial_deadline: int = 0
    
    def __post_init__(self):
        self.deadline = self.period
        self.initial_deadline = self.period
        self.remaining_time = self.wcets[0]

class RTScheduler:
    def __init__(self, tasks: List[Task], end_time: int, frequencies: List[int], powers: List[float]):
        self.tasks = tasks
        self.end_time = end_time
        self.frequencies = frequencies
        self.powers = powers
        self.schedule = []
        self.total_energy = 0
        self.idle_time = 0
        self.current_time = 0

    def calculate_energy(self, power: float, time: float) -> float:
        return (power/1000) * time

    def get_rm_priority(self, task: Task) -> int:
        return task.period

    def get_edf_deadline(self, task: Task, current_time: int) -> int:
        if current_time < task.initial_deadline:
            return task.initial_deadline
        
        # Calculate number of periods elapsed
        periods_elapsed = (current_time - task.initial_deadline) // task.period
        return task.initial_deadline + ((periods_elapsed + 1) * task.period)

    def update_task_state(self, current_time: int, algorithm: str):
        for task in self.tasks:
            if current_time >= task.next_release:
                if task.next_release > 0:  # Not the first release
                    task.remaining_time = task.wcets[0]
                    if algorithm == "EDF":
                        task.deadline = self.get_edf_deadline(task, current_time)
                task.next_release += task.period

    def schedule_tasks(self, algorithm: str, energy_efficient: bool = False) -> List[Tuple]:
        self.current_time = 0
        self.schedule = []
        
        # Initialize deadlines for EDF
        for task in self.tasks:
            task.next_release = 0
            task.deadline = task.period
            task.remaining_time = task.wcets[0]
        
        while self.current_time < self.end_time:
            self.update_task_state(self.current_time, algorithm)
            
            # Get ready tasks
            ready_tasks = [t for t in self.tasks 
                         if t.next_release - t.period <= self.current_time 
                         and t.remaining_time > 0]
            
            if not ready_tasks:
                next_release = min((t.next_release for t in self.tasks 
                                  if t.next_release > self.current_time), 
                                 default=self.end_time)
                idle_time = next_release - self.current_time
                energy = self.calculate_energy(self.powers[-1], idle_time)
                self.schedule.append((self.current_time, "IDLE", "IDLE", 
                                    idle_time, energy))
                self.idle_time += idle_time
                self.current_time = next_release
                continue
            
            # Select task based on algorithm
            if algorithm == "RM":
                current_task = min(ready_tasks, key=lambda t: t.period)
            else:  # EDF
                current_task = min(ready_tasks, 
                                 key=lambda t: self.get_edf_deadline(t, self.current_time))
            
            # Calculate execution time
            next_release = min((t.next_release for t in self.tasks 
                              if t.next_release > self.current_time), 
                             default=self.end_time)
            exec_time = min(current_task.remaining_time, 
                          next_release - self.current_time)
            
            # Energy efficient frequency selection
            if energy_efficient:
                available_time = current_task.deadline - self.current_time
                freq_idx = self.select_efficient_frequency(current_task, available_time)
                wcet = current_task.wcets[freq_idx]
                exec_time = min(wcet, exec_time)
            else:
                freq_idx = 0
                
            # Execute task
            energy = self.calculate_energy(self.powers[freq_idx], exec_time)
            self.schedule.append((self.current_time, current_task.name,
                                self.frequencies[freq_idx], exec_time, energy))
            self.total_energy += energy
            
            current_task.remaining_time -= exec_time
            self.current_time += exec_time

        return self.schedule

    def select_efficient_frequency(self, task: Task, available_time: int) -> int:
        valid_freqs = []
        for i, wcet in enumerate(task.wcets):
            if wcet <= available_time:
                energy = self.calculate_energy(self.powers[i], wcet)
                valid_freqs.append((energy, i))
        return min(valid_freqs, key=lambda x: x[0])[1] if valid_freqs else 0

    def print_schedule(self, algorithm: str, energy_efficient: bool = False):
        header = f"""-------------------------------------------
        Now running {"EE " if energy_efficient else ""}{algorithm}
-------------------------------------------
-------------------------------------------
        Printing Schedule Process
-------------------------------------------
{"<Time Started>".ljust(15)} {"<Task Name>".ljust(15)} {"<CPU Freq>".ljust(15)} {"<Runtime>".ljust(15)} {"<NRG Consumed>"}"""
        
        schedule_lines = []
        for time, task, freq, duration, energy in self.schedule:
            schedule_lines.append(
                f"{str(time).ljust(15)} {str(task).ljust(15)} {str(freq).ljust(15)} "
                f"{str(duration).ljust(15)} {f'{energy:.2f} J'}"
            )
        
        footer = f"""-------------------------------------------
        Additional Information
-------------------------------------------
Total Energy Consumption: {self.total_energy:.2f}J      Idle Rate: {(self.idle_time / self.end_time) * 100:.1f}%         Total Execution Time: {self.end_time}s"""
        
        output = "\n".join([header] + schedule_lines + ["", footer])
        print(output)
        
        filename = f"schedule_{'ee_' if energy_efficient else ''}{algorithm.lower()}.txt"
        with open(filename, "w") as f:
            f.write(output)

def parse_input(filename: str) -> Tuple[List[Task], int, List[int], List[float]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    parts = lines[0].strip().split()
    num_tasks = int(parts[0])
    end_time = int(parts[1])
    powers = [float(x) for x in parts[2:]]
    frequencies = [1188, 918, 648, 384]
    
    tasks = []
    for i in range(num_tasks):
        parts = lines[i+1].strip().split()
        tasks.append(Task(
            name=parts[0],
            period=int(parts[1]),
            wcets=[int(x) for x in parts[2:]]
        ))
    
    return tasks, end_time, frequencies, powers

def main():
    if len(sys.argv) < 3:
        print("Usage: python scheduler.py <input_file> <EDF|RM> [EE]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    algorithm = sys.argv[2].upper()
    energy_efficient = len(sys.argv) > 3 and sys.argv[3].upper() == "EE"
    
    tasks, end_time, frequencies, powers = parse_input(input_file)
    scheduler = RTScheduler(tasks, end_time, frequencies, powers)
    schedule = scheduler.schedule_tasks(algorithm, energy_efficient)
    scheduler.print_schedule(algorithm, energy_efficient)

if __name__ == "__main__":
    main()