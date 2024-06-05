from .api import EnergiBridgeRunner
from IPython.core.magic import register_cell_magic

@register_cell_magic
def measure_energy_time_cell(line, cell):
  runner = EnergiBridgeRunner()
  runner.start()

  # Get the current global and local namespaces
  ipython = get_ipython()
  exec_globals = ipython.user_global_ns
  exec_locals = ipython.user_ns

  try:
    exec(cell, exec_globals, exec_locals)
  except Exception as e:
    print(f"Error executing cell: {e}")

  # Stop the measurement
  energy, duration = runner.stop()

  # Display the results
  if energy:
    print("Energy consumption (J): ", energy)
  if duration:
    print("Execution time (s): ", duration)
