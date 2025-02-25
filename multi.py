import subprocess

# List of scripts to ru
scripts = ["evil.py", "group.py"]

# Start each script in a new process
processes = []
for script in scripts:
    try:
        process = subprocess.Popen(["python3", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)
        print(f"Started the{script} (PID: {process.pid})")
    except Exception as e:
        print(f"Failed to start {script}: {e}")

# Wait for all processes to complete
for process in processes:
    process.wait()
