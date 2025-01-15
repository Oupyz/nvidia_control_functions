# Nvidia control  script for setting core and memory clock offsets, fan speed, and auto fan control based on temperature for Nvidia GPUs.
# This script is compatible with Linux, Windows, and MacOS.
# This script requires root permission to run on Linux under Wayland.
# This script requires the pynvml library to be installed. Install it using pip install pynvml.
# Written by Elias Dadde 
# email: walkonfire81@yahoo.com
# github: github.com/Oupyz/Elias
# version 0.1


import os
import pynvml as nv
import sys

nv.nvmlInit()
handle = nv.nvmlDeviceGetHandleByIndex(0)
gpu_name = nv.nvmlDeviceGetName(handle)
fan_count = nv.nvmlDeviceGetNumFans(handle)
gpu_temperature = nv.nvmlDeviceGetTemperature(handle, nv.NVML_TEMPERATURE_GPU)
driver_version = nv.nvmlSystemGetDriverVersion()

def read_offset_core(prompt: str) -> int:
    """Prompt the user for an integer input."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def gpu_core_clock_control() -> None:
    """Adjust the GPU core clock offset."""
    clock = read_offset_core("Enter core clock offset in MHz: ")
    try:
        nv.nvmlDeviceSetGpcClkVfOffset(handle, clock)
        print(f"Core clock offset set to {clock} MHz.")
    except nv.NVMLError as e:
        print(f"Failed to set core clock offset: {str(e)}")

def gpu_memory_clock_control() -> None:
    """Adjust the GPU memory clock offset."""
    mem_clock = read_offset_core("Enter memory clock offset in MHz: ")
    try:
        nv.nvmlDeviceSetMemClkVfOffset(handle, mem_clock)
        print(f"Memory clock offset set to {mem_clock} MHz.")
    except nv.NVMLError as e:
        print(f"Failed to set memory clock offset: {str(e)}")

def fan_control() -> None:
    """Manually set fan speed."""
    while True:
        fan_speed = read_offset_core("Enter fan speed in % (0-100): ")
        if 0 <= fan_speed <= 100:
            break
        print("Invalid input. Fan speed must be between 0 and 100.")
    try:
        for i in range(fan_count):
            nv.nvmlDeviceSetFanSpeed_v2(handle, i, fan_speed)
        print(f"Fan speed set to {fan_speed}%.")
    except nv.NVMLError as e:
        print(f"Failed to set fan speed: {str(e)}")

def auto_fan_control_based_on_temp() -> None:
    """Automatically adjust fan speed based on GPU temperature."""
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
            fan_speed: int  = 55

        for i in range(fan_count):
            nv.nvmlDeviceSetFanSpeed_v2(handle, i, fan_speed)
        print(f"Auto fan control set to {fan_speed}% based on temperature.")
    except nv.NVMLError as e:
        print(f"Failed to set fan speed: {str(e)}")

def menu() -> None:
    """Display the menu and process user input."""
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
        print("You are running under X11. Root permission is not needed.")
    elif sys.platform == "win32":
        print("You are running under Windows.")
    elif sys.platform == "darwin":
        print("You are running under MacOS.")

    main()
