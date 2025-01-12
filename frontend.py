import tkinter as tk
from PIL import Image, ImageTk
import platform
import psutil
import GPUtil
from backend import get_motherboard_info, measure_download_speed, get_random_fortune

def create_gui():
    root = tk.Tk()
    root.title("PySystemReport")
    root.geometry("600x700")  # Set the window size to 600x500

    # Create a label to display the OS string
    os_string = platform.system() + " " + platform.release()
    os_label = tk.Label(root, text=f"Current OS: {os_string}")
    os_label.pack(pady=10)

    # Create a label to display the CPU info
    cpu_info = platform.processor()
    cpu_label = tk.Label(root, text=f"CPU: {cpu_info}")
    cpu_label.pack(pady=10)

    # Create a label to display the RAM info
    ram_info = f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB"
    ram_label = tk.Label(root, text=f"RAM: {ram_info}")
    ram_label.pack(pady=10)

    # Create a label to display the OS partition size
    partition_info = psutil.disk_usage('/').total / (1024 ** 3)
    partition_label = tk.Label(root, text=f"OS Partition Size: {partition_info:.2f} GB")
    partition_label.pack(pady=10)

    # Note: GPU information retrieval is platform dependent and may require additional libraries
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_info = gpus[0].name
        else:
            gpu_info = "No GPU found"
    except ImportError:
        gpu_info = "GPUtil not installed"

    gpu_label = tk.Label(root, text=f"GPU: {gpu_info}")
    gpu_label.pack(pady=10)

    # Create a label to display the current internet speed
    try:
        download_speed = measure_download_speed("http://ipv4.download.thinkbroadband.com/10MB.zip")
        speed_label = tk.Label(root, text=f"Download Speed: {download_speed:.2f} Mbps")
        speed_label.pack(pady=10)
    except:
        speed_label = tk.Label(root, text="Speedtest not available")
        speed_label.pack(pady=10)

    # Create a label to display the motherboard/PC manufacturer
    motherboard_info = get_motherboard_info()
    motherboard_label = tk.Label(root, text=f"Motherboard: {motherboard_info}")
    motherboard_label.pack(pady=10)

    # Load an image and display it in the window to match the OS type
    os_logo_path = ""
    if platform.system() == "Windows":
        os_logo_path = "logos/windows_logo.png"
    elif platform.system() == "Linux":
        os_logo_path = "logos/linux_logo.png"
    elif platform.system() == "Darwin":
        os_logo_path = "logos/macos_logo.png"

    if os_logo_path:
        os_logo_image = Image.open(os_logo_path)
        os_logo_image = os_logo_image.resize((100, 100), Image.LANCZOS)
        os_logo_photo = ImageTk.PhotoImage(os_logo_image)
        os_logo_label = tk.Label(root, image=os_logo_photo)
        os_logo_label.image = os_logo_photo  # Keep a reference
        os_logo_label.pack(side="bottom", pady=10)

    # Create a label to display the fortune
    fortune_label = tk.Label(root, text="", wraplength=500)
    fortune_label.pack(pady=10)

    # Create a button to generate a random fortune
    def show_fortune():
        fortune = get_random_fortune()
        fortune_label.config(text=fortune)

    fortune_button = tk.Button(root, text="Get Random Fortune", command=show_fortune, width=20, height=2, padx=10, pady=10)
    fortune_button.pack(pady=5)

    # Create a button to close the window
    close_button = tk.Button(root, text="Close", command=root.quit, width=20, height=2, padx=10, pady=10)
    close_button.pack(pady=20)

    root.mainloop()