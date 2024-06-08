from IPython import get_ipython
import pyEnergiBridge

# Ensure the magic is registered
ipython = get_ipython()

# Test the magic function
code = """
%%measure_energy_time_cell
from time import sleep
for i in range(5):
  print(i)
sleep(1)
"""
ipython.run_cell(code)

code = """
from time import sleep
%measure_energy_time_line sleep(1)
for i in range(5): print(i)
"""
ipython.run_cell(code)
