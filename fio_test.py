import os
import sys
from pathlib import Path
import subprocess
import time
import re

# model_dir = sys.argv[1]
# root = Path(model_dir)
# files = []
files = sys.argv[1:]
size_bytes = 0
procs = []
num_jobs = 1

# for f in root.iterdir():
#     if f.is_file() and f.name.endswith(".safetensors"):
#         files.append((f.name, f.stat().st_size))

files.sort()

t = time.time()
for fpath in files:
    fsize = os.path.getsize(fpath)
    size_bytes += fsize
    sub_size = fsize // num_jobs
    cmd = f"fio --name test --filename {fpath} --bs 4M --rw read --ioengine io_uring --iodepth 512 --direct 1 --numjobs {num_jobs} --offset 0 --offset_increment {sub_size} --size {sub_size}"
    print(cmd)
    proc = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
    procs.append(proc)

for proc in procs:
    return_code = proc.wait()
    if return_code != 0:
        print(f"Error: {proc.stderr.read()}")
        exit(1)
    lines = proc.stdout.read().strip().splitlines()
    last_line = lines[-1]
    #extract "run=222-222msec" from last_line, I need to match "run" and get 222
    # run_time = re.search(r"run=(\d+)-(\d+)msec", last_line).group(1)
    # t += int(run_time) * 1e-3

t = time.time() - t

print(f"Time taken: {t:.2f} seconds, Size: {size_bytes * 1e-9:.2f} GB, Throughput: {size_bytes * 1e-9 / t:.2f} GB/s")