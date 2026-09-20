#!/usr/bin/env python3
import sys
import time
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox

def is_chrome_running():
    # Check if Chrome or Chromium is running
    return subprocess.run(["pgrep", "-f", "chrome|chromium"], stdout=subprocess.DEVNULL).returncode == 0

def fill_ram_gradually(gib, chunk_mb=16, delay=0.1):
    """Slowly allocates memory in small chunks."""
    chunk_bytes = chunk_mb * 1024 * 1024
    total_bytes = int(gib * (1024**3))
    num_chunks = total_bytes // chunk_bytes
    
    print(f"[*] Starting gradual RAM allocation ({gib} GiB)...")
    ram_blocks = []
    
    for i in range(num_chunks):
        # Allocate and commit physical memory block
        ram_blocks.append(bytearray(b"\x01" * chunk_bytes))
        allocated_gib = ((i + 1) * chunk_bytes) / (1024**3)
        print(f"[+] Nom nom nom... Consumed {allocated_gib:.2f} GiB / {gib:.2f} GiB", end="\r")
        time.sleep(delay)
        
    print("\n[*] RAM fill complete. Chrome has met its match!")
    return ram_blocks

def show_funny_popup():
    """Displays a graphical warning window on Linux desktop environments."""
    root = tk.Tk()
    root.withdraw()  # Hide main window
    root.attributes("-topmost", True)  # Bring popup to front
    
    msg = (
        "🚨 ALERT: Chrome detected! 🚨\n\n"
        "Chrome tries to steal all your RAM, so I am eating it first to keep it safe.\n"
        "Please stand by while I beat Chrome to the punch..."
    )
    
    messagebox.showwarning("Potato Defense Mechanism", msg)
    root.destroy()

def main():
    if len(sys.argv) < 2:
        print("Usage: ./ramfiller.py <GiB> [--watch]")
        sys.exit(1)

    gib = float(sys.argv[1])
    watch = "--watch" in sys.argv

    if watch:
        print("[*] Monitoring for Chrome...")
        while not is_chrome_running():
            time.sleep(1)
        print("[!] Chrome detected!")

    # Show popup on a separate thread so it doesn't block the memory filling logic
    popup_thread = threading.Thread(target=show_funny_popup, daemon=True)
    popup_thread.start()

    # Fill RAM slowly (16 MB chunks every 0.05 seconds)
    ram_blocks = fill_ram_gradually(gib, chunk_mb=16, delay=0.05)

    if watch:
        print("\n[POTATO DEFENSE] Powering off system...")
        subprocess.run(["pkill", "-f", "chrome|chromium"])
        subprocess.run(["systemctl", "poweroff"])
        sys.exit(0)

    try:
        input("\nPress Enter or Ctrl+C to release RAM...")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()