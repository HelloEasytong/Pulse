import subprocess
import os
from colorama import Fore, Style

def calculate(operation, num1, num2):
    try:
        result = subprocess.run(
            ['calculator', operation, str(num1), str(num2)],
            check=True,
            capture_output=True,
            text=True
        )
        return float(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() or "Unknown error occurred"
        print(Fore.RED + f"{error_msg}" + Style.RESET_ALL)
        return None