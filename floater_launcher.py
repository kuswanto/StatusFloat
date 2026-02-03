# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import obspython as obs
import subprocess
import os

# --- SETTINGS ---
# Path to your Python 3.11.x instalation path
PYTHON_EXE = r"C:\ProgramData\miniconda3\python.exe"
SCRIPT_NAME = "obs_floater.py"

process = None

def script_load(settings):
    global process
    dir_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(dir_path, SCRIPT_NAME)

    # Use shell=True to help Windows handle the window creation
    try:
        process = subprocess.Popen(
            f'"{PYTHON_EXE}" "{full_path}"',
            cwd=dir_path,
            shell=True
        )
        print("Launcher: Overlay started via shell.")
    except Exception as e:
        print(f"Launcher Error: {e}")

def script_unload():
    global process
    if process:
        # Since we used shell=True, we kill the process tree
        subprocess.call(['taskkill', '/F', '/T', '/PID', str(process.pid)])