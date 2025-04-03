import subprocess
import time
import os
import signal

BOT_SCRIPT = "legacyattack2.py"

def start_bot():
    print("Starting the bot...")
    return subprocess.Popen(f"python3 {BOT_SCRIPT}", shell=True, stdout=None, stderr=None, stdin=None, preexec_fn=os.setsid)

def stop_bot(process):
    print("Stopping the bot...")
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

while True:
    bot_process = start_bot()
    time.sleep(600)  # 10 minutes
    stop_bot(bot_process)
