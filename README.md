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

## Configuration

By default, pyEnergiBridge looks for the `EnergiBridge` binary in a predefined path. You can customize the path to the EnergiBridge binary using configuration files. The configuration files can be placed in the user's home directory or in the project directory.

### 1. Home Directory Configuration:
Create a file named `.pyenergibridge_config.json` in your home directory:

```json
{
    "binary_path": "/custom/path/to/EnergiBridge/home"
}
```

### 2. Project Directory Configuration:
Create a file named `pyenergibridge_config.json` in your project directory:

```json
{
    "binary_path": "/custom/path/to/EnergiBridge/home"
}
```

pyEnergiBridge will first look for the configuration file in the project directory, and if it is not found, it will look for the configuration file in the home directory. If no configuration files are found, it will check if `EnergiBridge` is available in the system's PATH. If none of these methods provide a valid path, it will raise a `FileNotFoundError`.

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
