from IPython import get_ipython
import pyEnergiBridge

# Ensure the magic is registered
ipython = get_ipython()

# Test the magic function
code = """
%%measure_energy_time_cell
for i in range(5):
  print(i)
"""
ipython.run_cell(code)
