from .api import EnergiBridgeRunner
from IPython.core.magic import register_cell_magic, register_line_magic
from IPython.display import display, HTML

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
  _display_results(ipython, energy, duration)

@register_line_magic
def measure_energy_time_line(line):
  runner = EnergiBridgeRunner()
  runner.start()
  
  # Get the current global and local namespaces
  ipython = get_ipython()
  exec_globals = ipython.user_global_ns
  exec_locals = ipython.user_ns
  
  try:
      exec(line, exec_globals, exec_locals)
  except Exception as e:
      print(f"Error executing line: {e}")
  
  # Stop the measurement
  energy, duration = runner.stop()
  _display_results(ipython, energy, duration)


def _display_results(ipython, energy, duration):
  if ipython.__class__.__name__ == 'ZMQInteractiveShell':
    # Create the result HTML
    result_html = f"""
    <div style='border:1px solid #ccc; padding:0 10px; margin:10px 0;'>
        <h4>Measurement Results</h4>
        <p><strong>🌿 Energy:</strong> {energy} J
        <br/><strong>⏰ Time:</strong> {duration} s</p>
    </div>
    """
    display(HTML(result_html))
  else:
    # Display the results
    print("Energy consumption (J): ", energy)
    print("Execution time (s): ", duration)
