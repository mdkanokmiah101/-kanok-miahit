import subprocess, sys, os
os.chdir("/root/kanok-miahit")
result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True, timeout=30)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("RC:", result.returncode)
sys.exit(0)
