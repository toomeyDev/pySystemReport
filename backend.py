import platform
import subprocess
import requests
import time
import shutil

# Import wmi only if on Windows
if platform.system() == "Windows":
    import wmi

def get_motherboard_info():
    if platform.system() == "Windows":
        try:
            c = wmi.WMI()
            for board in c.Win32_BaseBoard():
                manufacturer = board.Manufacturer
                product = board.Product
                return f"{manufacturer} {product}"
        except Exception as e:
            return f"Error: {e}"
    else:
        try:
            result = subprocess.run(['sudo', 'dmidecode', '-t', 'baseboard'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                output = result.stdout
                manufacturer = ""
                product = ""
                for line in output.split('\n'):
                    if "Manufacturer" in line:
                        manufacturer = line.split(":")[1].strip()
                    if "Product Name" in line:
                        product = line.split(":")[1].strip()
                return f"{manufacturer} {product}"
            else:
                return "dmidecode command failed"
        except Exception as e:
            return f"Error: {e}"

def measure_download_speed(url, timeout=10):
    start_time = time.time()
    response = requests.get(url, stream=True, timeout=timeout)
    total_size = 0
    for chunk in response.iter_content(chunk_size=1024):
        total_size += len(chunk)
    end_time = time.time()
    duration = end_time - start_time
    speed_mbps = (total_size * 8) / (1024 * 1024 * duration)
    return speed_mbps

def get_random_fortune():
    if shutil.which("fortune") is not None:
        try:
            result = subprocess.run(['fortune'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return "Fortune command failed"
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Fortune command not found. Please install it using 'sudo apt-get install fortune-mod' on Debian-based systems or 'sudo dnf install fortune-mod' on Fedora-based systems."