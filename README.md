# pyEnergiBridge
Python wrapper to collect software energy consumption data using EnergiBridge.

How to use it:

#### Install

```
git clone https://github.com/luiscruz/pyEnergiBridge.git
pip install .
```

#### Within your python code


This is a basic example.

```
import time
from pyEnergiBridge.api import EnergiBridgeRunner

runner = EnergiBridgeRunner()
runner.start(results_file="results.csv")

time.sleep(2) # or any other task

energy, duration = runner.stop()
print(f"Energy consumption (J): {energy}; execution time (s): {duration}")


```


This is a basic example using the decorator.
```
import time
from pyEnergiBridge.api import with_energibridge

@with_energibridge(results_file="results.csv")
def my_task():
    # Simulate a task running for a short period of time
    time.sleep(2)
    print("Task completed.")

my_task()

```
Confirm that the full sample of energy data was stored in "results.csv".

