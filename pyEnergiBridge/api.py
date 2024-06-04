import subprocess
import os
import signal
import platform
from functools import wraps
import time

#from IPython.core.magic import register_cell_magic

class EnergiBridgeRunner:
    def __init__(self, results_file=None, command="dup"):
        self.process = None

    def start(self, results_file=None, command="nop"):
        binary_path = os.path.join(os.path.dirname(__file__), '..', 'bin', 'energibridge')
        args = ["--summary"]
        if results_file:
            print(f"Results will be printed to {results_file}")
            args.extend(["-o", results_file])
        args.append(command)
        try:
            # Mocking subprocess.Popen to simulate the process
            self.process = subprocess.Popen(["python", "-c", "import time; time.sleep(2); print('Energy consumption in joules: 123.45 for 67.89 sec')"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"EnergiBridge started with PID: {self.process.pid}")
        except Exception as e:
            print(f"Failed to start EnergiBridge: {e}")

    def stop(self):
        if self.process:
            try:
                if platform.system() == "Windows":
                    self.process.terminate()  # Use terminate on Windows
                else:
                    self.process.send_signal(signal.SIGINT)  # Use SIGINT on Unix-like systems

                stdout, stderr = self.process.communicate()  # Wait for process to terminate
                print("EnergiBridge stopped.")
                return self._process_stdout(stdout)
            except Exception as e:
                print(f"Failed to stop EnergiBridge: {e}")
                return None, None
        else:
            print("EnergiBridge is not running.")
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