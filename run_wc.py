import os
os.chdir("/root/kanok-miahit")
with os.popen("wc -l src/app/blog/data.js 2>&1") as f:
    print(f.read())
