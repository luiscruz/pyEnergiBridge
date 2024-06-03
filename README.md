# pyEnergiBridge

pyEnergiBridge is a Python wrapper that enables the collection of software energy consumption data using EnergiBridge.

## Installation

You can install pyEnergiBridge via pip. First, clone the repository:

```bash
git clone https://github.com/luiscruz/pyEnergiBridge.git
cd pyEnergiBridge
```

Then, install the package using pip:
```bash
pip install .
```

## Usage

### Basic Usage
To collect energy consumption data within your Python code, follow these steps:

```python
import time
from pyEnergiBridge.api import EnergiBridgeRunner

runner = EnergiBridgeRunner()
runner.start(results_file="results.csv")

# Perform some task
time.sleep(2)

# Stop the data collection and retrieve results
energy, duration = runner.stop()
print(f"Energy consumption (J): {energy}; Execution time (s): {duration}")
```

### Using Decorator
You can also use a decorator to simplify the process:

```python
import time
from pyEnergiBridge.api import with_energibridge

@with_energibridge(results_file="results.csv")
def my_task():
    # Simulate a task running for a short period of time
    time.sleep(2)
    print("Task completed.")

# Execute the task
my_task()
```
Make sure to check the "results.csv" file to confirm that the energy consumption data has been stored successfully.
