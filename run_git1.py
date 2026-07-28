import os, sys
os.chdir("/root/kanok-miahit")
# Just read the diff
with os.popen("cd /root/kanok-miahit && git diff c822841~1 c822841 -- src/app/blog/data.js 2>&1") as f:
    data = f.read()
print(data[:5000])
print("---TOTAL LENGTH:", len(data))
