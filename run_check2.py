import subprocess
result = subprocess.run("cd /root/kanok-miahit && git log --oneline -5", shell=True, capture_output=True, text=True, timeout=30)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)
