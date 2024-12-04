# Real-Time Task Scheduler with DVFS - Python Implementation

## Overview
This project implements a real-time task scheduler with Dynamic Voltage and Frequency Scaling (DVFS) capabilities. The scheduler supports four scheduling algorithms:
- Rate-Monotonic (RM)
- Earliest Deadline First (EDF)
- Energy-Efficient Rate-Monotonic (EE RM)
- Energy-Efficient Earliest Deadline First (EE EDF)

## Requirements
- Python 3.7 or higher
- No additional packages required (uses standard library only)

## Installation
1. Clone or download the repository
2. Ensure `scheduler.py` and your input files are in the same directory

## Usage
Run the scheduler using the following command format:
```bash
python scheduler.py <input_file> <EDF|RM> [EE]
```

### Parameters:
- `<input_file>`: Path to the input text file
- `<EDF|RM>`: Scheduling algorithm (EDF or RM)
- `[EE]`: Optional parameter for energy-efficient mode

### Example Commands:
```bash
python scheduler.py input1.txt EDF
python scheduler.py input1.txt RM
python scheduler.py input1.txt EDF EE
python scheduler.py input1.txt RM EE
```

## Input File Format
The input file should follow this format:

First line:
```
<# of tasks> <execution time> <power@1188MHz> <power@918MHz> <power@648MHz> <power@384MHz> <idle power>
```

Subsequent lines (one per task):
```
<task name> <period/deadline> <WCET@1188MHz> <WCET@918MHz> <WCET@648MHz> <WCET@384MHz>
```

Example input file:
```
5 1000 625 447 307 212 84
w1 520 53 66 89 141
w2 220 40 50 67 114
w3 500 104 134 184 313
w4 200 57 74 103 175
w5 300 35 45 62 104
```

## Output
The program generates two types of output:

1. Console output showing:
   - Schedule process
   - Task execution details
   - Energy consumption
   - Idle time percentage
   - Total execution time

2. Text file output:
   - `schedule_edf.txt` for EDF scheduling
   - `schedule_rm.txt` for RM scheduling
   - `schedule_ee_edf.txt` for EE EDF scheduling
   - `schedule_ee_rm.txt` for EE RM scheduling

### Output Format:
```
-------------------------------------------
        Now running [Algorithm]
-------------------------------------------
-------------------------------------------
        Printing Schedule Process
-------------------------------------------
<Time Started>   <Task Name>     <CPU Freq>      <Runtime>       <NRG Consumed>
[Schedule entries...]

-------------------------------------------
        Additional Information
-------------------------------------------
Total Energy Consumption: X.XX J    Idle Rate: XX.X%    Total Execution Time: XXXs
```

## Algorithms
### Rate-Monotonic (RM)
- Fixed priority scheduling based on task periods
- Higher priority for shorter periods
- Preemptive scheduling

### Earliest Deadline First (EDF)
- Dynamic priority scheduling based on absolute deadlines
- Preemptive scheduling
- Optimal for single processor systems

### Energy-Efficient Variants (EE)
- Uses DVFS to reduce energy consumption
- Selects lowest possible frequency while meeting deadlines
- Maintains scheduling order of base algorithms

## Error Handling
The program includes basic error handling for:
- Invalid input file format
- Missing command line arguments
- Invalid scheduling algorithm selection

## Notes
- All power values in input file should be in milliwatts (mW)
- All time values should be in seconds
- The program assumes task deadlines equal their periods