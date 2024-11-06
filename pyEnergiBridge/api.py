import os
import subprocess
import signal
from functools import wraps
import json
from pathlib import Path
import shutil
import time
import logging

class EnergiBridgeRunner:
  def __init__(self, results_file=None, command="dup", verbose=True):
    self.process = None
    self.default_path = Path('..') / "bin" / "EnergiBridge"
    self.command_name = "EnergiBridge"
    self.config_path_home = Path.home() / '.pyenergibridge_config.json'
    self.config_path_project = Path('.') / 'pyenergibridge_config.json'
    self.binary_path = self._load_config()
    self.logger = logging.getLogger(self.__class__.__name__)

    if verbose:
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
    
  def _load_config(self):
    config = {}

    # Load config from home directory if it exists
    if self.config_path_home.exists():
        with open(self.config_path_home, 'r') as f:
            config.update(json.load(f))

    # Load config from project directory if it exists
    if self.config_path_project.exists():
        with open(self.config_path_project, 'r') as f:
            config.update(json.load(f))

    # Return the binary path from config or default if not specified
    binary_path = config.get('binary_path', self.default_path)

    # Check if the binary path is a command available in PATH
    if shutil.which(binary_path) is not None:
        return binary_path

    # Otherwise, fall back to the default path if it exists
    if shutil.which(self.command_name) is not None:
        return self.command_name

    # If neither the config path nor the command is found, raise an error
    if not Path(binary_path).exists():
        raise FileNotFoundError(f"Could not find EnergiBridge binary at {binary_path}. Please check your configuration.")

    return binary_path

  def start(self, results_file=None, command=["sleep", "1000000"]): #timeoout 100 days
    args = ["--summary"]
    if results_file:
      self.logger.info(f"Results will be printed to {results_file}")
      args.extend(["-o", results_file])
    args.extend(command)

    try:
      self.process = subprocess.Popen([self.binary_path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
      self.logger.info(f"Running EnergiBridge from: {self.binary_path}; started with PID: {self.process.pid}")
    except OSError as e:
      raise RuntimeError(f"Failed to start EnergiBridge: {e}") from e

  def stop(self):
    if self.process:
      try:
        self.process.terminate()  # Use terminate for all platforms
        stdout, stderr = self.process.communicate()  # Wait for process to terminate
        self.logger.info("EnergiBridge stopped.")
        return self._process_stdout(stdout)
      except Exception as e:
        self.logger.info(f"Failed to stop EnergiBridge: {e}")
        return None, None
    else:
      self.logger.info("EnergiBridge is not running.")
      return None, None

  def _process_stdout(self, output):
    lines = output.split('\n')
    for line in lines:
      if "Energy consumption in joules: " in line:
        parts = line.split(":")
        energy_str, seconds_str = parts[1].strip().split(" for ")
        energy_consumption = float(energy_str)
        duration = float(seconds_str.split(" sec")[0])
        return energy_consumption, duration
    return None, None

def with_energibridge(*eb_args, **eb_kwargs):
  def decorator(func):
    @wraps(func)
    def wrapper(*func_args, **func_kwargs):
      runner = EnergiBridgeRunner()
      runner.start(*eb_args, **eb_kwargs)

      try:
        result = func(*func_args, **func_kwargs)
      finally:
        energy, duration = runner.stop()
        if energy:
          print("Energy consumption (J): ", energy)
        if duration:
          print("Execution time (s): ", duration)

      return result
    return wrapper
  return decorator

# Playground
@with_energibridge(results_file="results.csv")
def my_task():
  # Simulate a task running for a short period of time
  time.sleep(2)
  print("Task completed.")

if __name__ == "__main__":
  my_task()
