# Nvidia control  script for setting core and memory clock offsets, fan speed, and auto fan control based on temperature for Nvidia GPUs.
# This script is compatible with Linux, Windows, and MacOS.
# This script requires root permission to run on Linux under Wayland.
# This script requires the pynvml library to be installed. Install it using pip install pynvml.
# Written by Elias Dadde 
# email: walkonfire81@yahoo.com
# github: github.com/Oupyz/Elias
# version 0.2
# This script must have pip3 installed and hostnamectl installed for the script to function correctly
# its written to work on openSUSE and most linux distributions but it doesn't check for other distros dependencies as i'am not sure how other distros manage their python packages and modules .


import os
import pynvml as nv
import sys
import time
import subprocess as sb 

nv.nvmlInit()

gpu_id = nv.nvmlDeviceGetHandleByIndex(0)
gpu_name = nv.nvmlDeviceGetName(gpu_id)
fan_count = nv.nvmlDeviceGetNumFans(gpu_id)
driver_version = nv.nvmlSystemGetDriverVersion()

def restarting_script() -> None:
    
    script_path: str  = os.path.abspath(__file__)
    cmd: str = sys.executable
    sb.run([cmd, script_path], capture_output=True, text=True)
    
def check_dependencies() -> bool:
  
    pip_cmd = "pip3"
    dependency = "pynvml"
    os_check_cmd = "hostnamectl"
    os_match = "openSUSE"

    print("Checking dependencies...")

    result = sb.run([pip_cmd, "show", dependency], capture_output=True, text=True)
    if result.returncode == 0:
        print("All dependencies are already installed.")
        return True

    print("Detecting operating system...")
    os_result = sb.run([os_check_cmd], capture_output=True, text=True)
    if os_result.returncode == 0:
        for line in os_result.stdout.splitlines():
            if os_match in line:
                print(f"Detected {os_match}. Installing dependencies with --break-system-packages...")
                install_result = sb.run([pip_cmd, "install", dependency, "--break-system-packages"], capture_output=True, text=True)
                if install_result.returncode == 0:
                    print("Dependencies installed successfully.")
                    return True
                else:
                    print(f"Failed to install {dependency} on {os_match}.")
                    return False

    print("Installing dependencies...")
    install_result = sb.run([pip_cmd, "install", dependency], capture_output=True, text=True)
    if install_result.returncode == 0:
        print("Dependencies installed successfully.")
        return True

    print("Failed to install dependencies.")
    return False

    
    


def read_offset_core(yourinput: str) -> int:
    
  
    while True:
        try:
            return int(input(yourinput))
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def gpu_core_clock_control() -> None:
    
    
    clock = read_offset_core("Enter core clock offset in MHz: ")
    try:
        nv.nvmlDeviceSetGpcClkVfOffset(gpu_id, clock)
        print(f"Core clock offset set to {clock} MHz.")
    except nv.NVMLError as e:
        print(f"Failed to set core clock offset: {str(e)}")

def gpu_memory_clock_control() -> None:
    
    
    mem_clock = read_offset_core("Enter memory clock offset in MHz: ")
    try:
        nv.nvmlDeviceSetMemClkVfOffset(gpu_id, mem_clock)
        print(f"Memory clock offset set to {mem_clock} MHz.")
    except nv.NVMLError as e:
        print(f"Failed to set memory clock offset: {str(e)}")

def fan_control() -> None:
   
    while True:
        fan_speed = read_offset_core("Enter fan speed in % (0-100): ")
        if 0 <= fan_speed <= 100:
            break
        print("Invalid input. Fan speed must be between 0 and 100.")
    try:
        for i in range(fan_count):
            nv.nvmlDeviceSetFanSpeed_v2(gpu_id, i, fan_speed)
        print(f"Fan speed set to {fan_speed}%.")
    except nv.NVMLError as e:
        print(f"Failed to set fan speed: {str(e)}")

def auto_fan_control_based_on_temp() -> None:
   
    
    print(f"\n""Press Crtl+C for the auto fan speed adjustment based on your gpu temps .")
    
    while True:
     time.sleep(10)   
     gpu_temperature = nv.nvmlDeviceGetTemperature(gpu_id, nv.NVML_TEMPERATURE_GPU)
     try:
        if gpu_temperature <= 30:
            fan_speed: int  = 30
        elif gpu_temperature <= 40:
            fan_speed: int  = 45
        elif gpu_temperature <= 50:
            fan_speed: int  = 60
        elif gpu_temperature <= 60:
            fan_speed: int  = 70
        elif gpu_temperature <= 70:
            fan_speed: int  = 90
        else:
            fan_speed: int  = 100
    
        for i in range(fan_count):
            nv.nvmlDeviceSetFanSpeed_v2(gpu_id, i, fan_speed)
     except nv.NVMLError as e:
        print(f"Failed to set fan speed: {str(e)}")
     
def menu() -> None:
   
    check_dependencies()
    
    while True:
        print("\nMenu:")
        print("1. Set Core Clock Offset")
        print("2. Set Memory Clock Offset")
        print("3. Set Manual Fan Speed")
        print("4. Auto Fan Control")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            gpu_core_clock_control()
        elif choice == "2":
            gpu_memory_clock_control()
        elif choice == "3":
            fan_control()
        elif choice == "4":
            auto_fan_control_based_on_temp()
        elif choice == "5":
            print("Exiting the script.")
            nv.nvmlShutdown()
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

def main():
    
    """Main function to display GPU information and launch the menu."""
    
    print(f"NVIDIA GPU Overclocking Script and Fan Control")
    print(f"Driver Version: {driver_version}")
    print(f"GPU Name: {gpu_name}\n")
    menu()

if __name__ == "__main__":
    
    if sys.platform == "linux":
        print("You are running under Linux.")
    if os.environ.get("XDG_SESSION_TYPE") == "wayland":
        print("Warning: You are running under Wayland. Root permission is needed.")
    elif os.environ.get("XDG_SESSION_TYPE") == "x11":
        print("You are running under X11, Root permission is not needed.")
    elif sys.platform == "win32":
        print("You are running under Windows.")
    elif sys.platform == "darwin":
        print("You are running under MacOS.")
   
main()
    