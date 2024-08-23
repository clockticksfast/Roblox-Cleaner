import os
import shutil
import subprocess
import ctypes
import sys
import requests
import time

def is_admin():
    """Check if the script is run as an administrator."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    """Relaunch the script with administrator privileges."""
    if not is_admin():
        # Relaunch the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

def do_clear(log_name):
    subprocess.run(['wevtutil.exe', 'cl', log_name])  # Clear the event log

# Request administrator permissions
run_as_admin()

# Initialize counters for cleaned items
cleaned_temp_files = 0
cleaned_temp_dirs = 0
cleaned_registry_keys = 0
deleted_roblox_instances = 0
deleted_exploit_instances = 0
cleared_event_logs = 0

# Roblox and Exploit instances
RobloxInstances = {
    "Roblox": os.path.expandvars(r"%localappdata%\Roblox"),
    "Bloxstrap": os.path.expandvars(r"%localappdata%\Bloxstrap")
}

ExploitInstances = {
    "Solara": os.path.expandvars(r"C:\ProgramData\Solara"),
    "OldSolara": os.path.expandvars(r"C:\ProgramData\Solara.Dirh"),
    "OldOldsolara": os.path.expandvars(r"%temp%\Solara.Dirh"),
    "Wave": os.path.expandvars(r"%localappdata%\Wave")
}

# Clean Prefetch folder
prefetch_path = r"C:\Windows\Prefetch"
if os.path.exists(prefetch_path):
    for filename in os.listdir(prefetch_path):
        file_path = os.path.join(prefetch_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            continue

default_recent_path = r"C:\Users\Default\AppData\Roaming\Microsoft\Windows\Recent"
user_recent_path = fr"C:\Users\{os.getlogin()}\AppData\Roaming\Microsoft\Windows\Recent"

if os.path.exists(default_recent_path):
    shutil.rmtree(default_recent_path)
if os.path.exists(user_recent_path):
    shutil.rmtree(user_recent_path)

# Delete Roblox instances
for Name, Path in RobloxInstances.items():
    if os.path.exists(Path):
        shutil.rmtree(Path)
        deleted_roblox_instances += 1

# Delete Exploit instances
for Name, Path in ExploitInstances.items():
    if os.path.exists(Path):
        shutil.rmtree(Path)
        deleted_exploit_instances += 1

# Clean registry keys
keys = [
    r"HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache",
    r"HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags",
    r"HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\BagMRU",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Persisted",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\MUICache",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRULegacy",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU",
    r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist"
]
for key in keys:
    try:
        subprocess.run(["reg", "delete", key, "/f"], check=True)
        cleaned_registry_keys += 1
    except subprocess.CalledProcessError:
        continue

# Clean Temp folder
temp_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'Temp')
for item in os.listdir(temp_dir):
    item_path = os.path.join(temp_dir, item)
    try:
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
            cleaned_temp_dirs += 1
        else:
            os.remove(item_path)
            cleaned_temp_files += 1
    except Exception:
        continue

print('Please wait as Event Log Entries are being deleted...')

# Run wevtutil to get the event log names
wevtutil_output = subprocess.check_output(['wevtutil.exe', 'el'], text=True)

# Process each event log name
for line in wevtutil_output.splitlines():
    do_clear(line.strip())  # Clear the event log
    cleared_event_logs += 1

# Print the summary of cleaned items
print('Successfully cleaned your computer!')
print('Supported Executors: Solara, Wave')
print('Supported Instances: Roblox, Bloxstrap')
print('Summary of what was cleaned:')
print(f"- Temp files cleaned: {cleaned_temp_files}")
print(f"- Temp directories cleaned: {cleaned_temp_dirs}")
print(f"- Registry keys deleted: {cleaned_registry_keys}")
print(f"- Roblox instances deleted: {deleted_roblox_instances}")
print(f"- Exploit instances deleted: {deleted_exploit_instances}")
print(f"- Event logs cleared: {cleared_event_logs}")

print("")
print("Please wait as we reinstall roblox for you")
installer_url = "https://github.com/clockticksfast/Roblox-Cleaner/raw/main/RobloxPlayerInstaller.exe"
installer_path = os.path.join(os.getenv('TEMP'), "RobloxPlayerInstaller.exe")

print("Downloading Roblox installer...")
response = requests.get(installer_url)
with open(installer_path, 'wb') as file:
    file.write(response.content)
print("Download complete.")

print("Running Roblox installer...")
subprocess.run([installer_path], check=True)

# Clean up the installer file
if os.path.exists(installer_path):
    os.remove(installer_path)
    print("Cleaned up installer file.")
print('Exiting in 10 seconds...')

time.sleep(10)
