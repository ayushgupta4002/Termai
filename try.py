import subprocess
import sys

process = subprocess.Popen(
    "npx create-next-app@latest",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True,
    shell=True  # Run in Windows shell
)


while True:
    for line in iter(process.stdout.readline, ""):
        sys.stdout.write(line)
        sys.stdout.flush()

process.stdout.close()
process.wait()
