import subprocess
import sys

cmd = "cd /root/kanok-miahit && git log --oneline -5"
result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
