import os
import time
import pyautogui
import subprocess

# Function to send fake UI interaction
def keep_alive():
    while True:
        pyautogui.press("shift")  # UI ko active rakhne ke liye Shift press karega
        print("Fake interaction sent!")
        time.sleep(120)  # Har 2 min me ek baar trigger karega

# Fork process to background
def fork_terminal():
    pid = os.fork()
    if pid > 0:
        exit()  # Parent process exit karega, child process background me chalega

# Start the fake interaction in a separate background process
def start_keep_alive():
    subprocess.Popen(keep_alive)

# Run bot script
def start_bot():
    bot_script = "bot.py"  # Teri bot wali script ka naam
    print(f"Starting bot script: {bot_script}")
    subprocess.run(["python3", bot_script])

# Fork terminal
fork_terminal()

# Start keep-alive process
start_keep_alive()

# Start bot script
start_bot()
