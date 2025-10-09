#!/usr/bin/env python3
"""
8BitDo Firmware Updater
Automates the process of downloading and flashing firmware for 8BitDo gamepads on Linux
"""

import requests
import subprocess
import sys
import json
import os
from pathlib import Path

# Gamepad types mapping
GAMEPADS = {
    "1": {"name": "Arcade Stick", "type": 34},
    "2": {"name": "Arcade Stick Receiver", "type": 35},
    "3": {"name": "F30 GamePad", "type": 2},
    "4": {"name": "F30 Arcade Stick", "type": 5},
    "5": {"name": "F30 Pro", "type": 1},
    "6": {"name": "Lite GamePad", "type": 28},
    "7": {"name": "M30", "type": 23},
    "8": {"name": "N30 GamePad", "type": 2},
    "9": {"name": "N30 NS GamePad", "type": 18},
    "10": {"name": "N30 Pro", "type": 1},
    "11": {"name": "N30 Pro 2", "type": 13},
    "12": {"name": "Pro 2", "type": 33},
    "13": {"name": "Pro 2 Wired", "type": 37},
    "14": {"name": "SF30 Pro", "type": 9},
    "15": {"name": "SN30 GamePad", "type": 3},
    "16": {"name": "SN30 Pro+", "type": 25},
    "17": {"name": "SN30 Pro", "type": 9},
}

API_URL = "http://dl.8bitdo.com:8080/firmware/select"
DOWNLOAD_URL = "http://dl.8bitdo.com:8080"


def print_header():
    """Print a nice header"""
    print("\n" + "=" * 60)
    print("  8BitDo Firmware Updater")
    print("=" * 60 + "\n")


def display_gamepads():
    """Display available gamepad options"""
    print("Available gamepads:\n")
    for key, gamepad in GAMEPADS.items():
        print(f"  {key:2}. {gamepad['name']}")
    print()


def select_gamepad():
    """Prompt user to select their gamepad"""
    while True:
        choice = input("Enter the number of your gamepad: ").strip()
        if choice in GAMEPADS:
            return GAMEPADS[choice]
        print("Invalid selection. Please try again.\n")


def fetch_firmware_list(gamepad_type, include_beta=False):
    """Fetch available firmware versions from 8BitDo API"""
    print(f"\nFetching firmware list for {gamepad_type}...")
    
    headers = {
        'Type': str(gamepad_type),
        'Beta': '1' if include_beta else '0'
    }
    
    try:
        response = requests.post(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('msgState') != 1:
            print(f"Error from API: {data.get('error', 'Unknown error')}")
            return None
        
        return data.get('list', [])
    except requests.RequestException as e:
        print(f"Error fetching firmware list: {e}")
        return None


def display_firmware_versions(firmware_list):
    """Display available firmware versions"""
    if not firmware_list:
        print("No firmware versions found.")
        return None
    
    print("\nAvailable firmware versions:\n")
    for idx, fw in enumerate(firmware_list, 1):
        version = fw.get('version', 'Unknown')
        date = fw.get('date', 'Unknown')
        size_kb = fw.get('fileSize', 0) / 1024
        beta = " (BETA)" if fw.get('beta') else ""
        print(f"  {idx}. Version {version} - {date} ({size_kb:.1f} KB){beta}")
    
    return firmware_list


def select_firmware(firmware_list):
    """Prompt user to select firmware version"""
    while True:
        try:
            choice = input("\nEnter the number of the firmware to download (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(firmware_list):
                return firmware_list[idx]
            print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def download_firmware(firmware):
    """Download the selected firmware file"""
    file_path = firmware.get('filePathName')
    if not file_path:
        print("Error: No file path found in firmware data")
        return None
    
    url = f"{DOWNLOAD_URL}{file_path}"
    filename = Path(file_path).name
    
    print(f"\nDownloading firmware: {filename}...")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Firmware downloaded successfully: {filename}")
        return filename
    except requests.RequestException as e:
        print(f"Error downloading firmware: {e}")
        return None


def get_gamepad_device_id():
    """Get the device ID from fwupdmgr"""
    print("\nSearching for 8BitDo gamepad...")
    
    try:
        result = subprocess.run(
            ['fwupdmgr', 'get-devices', '--json'],
            capture_output=True,
            text=True,
            check=True
        )
        
        devices = json.loads(result.stdout)
        
        # Look for 8BitDo device
        for device in devices.get('Devices', []):
            vendor = device.get('Vendor', '').lower()
            if '8bitdo' in vendor or '8bit' in vendor:
                device_id = device.get('DeviceId')
                name = device.get('Name', 'Unknown')
                version = device.get('Version', 'Unknown')
                
                print(f"\n✓ Found: {name}")
                print(f"  Current version: {version}")
                print(f"  Device ID: {device_id}")
                
                return device_id
        
        print("No 8BitDo gamepad found.")
        return None
        
    except subprocess.CalledProcessError as e:
        print(f"Error running fwupdmgr: {e}")
        print("Make sure fwupd is installed and you have the necessary permissions.")
        return None
    except json.JSONDecodeError:
        print("Error parsing fwupdmgr output. Trying alternative method...")
        return get_device_id_fallback()


def get_device_id_fallback():
    """Fallback method to get device ID from text output"""
    try:
        result = subprocess.run(
            ['fwupdmgr', 'get-devices'],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.split('\n')
        device_id = None
        
        for i, line in enumerate(lines):
            if '8bitdo' in line.lower():
                # Look for Device ID in nearby lines
                for j in range(max(0, i-5), min(len(lines), i+10)):
                    if 'Device ID:' in lines[j]:
                        device_id = lines[j].split('Device ID:')[1].strip()
                        break
                if device_id:
                    print(f"\n✓ Found device ID: {device_id}")
                    return device_id
        
        return None
    except subprocess.CalledProcessError:
        return None


def flash_firmware(firmware_file, device_id):
    """Flash the firmware to the gamepad"""
    print("\nFlashing firmware to gamepad...")
    print("This may take a minute. Please do not disconnect the gamepad.")
    print("You may be prompted for your sudo password...\n")
    
    try:
        # Run with sudo for proper permissions
        result = subprocess.run(
            ['sudo', 'fwupdtool', 'install-blob', firmware_file, device_id],
            text=True
        )
        
        if result.returncode == 0:
            print("\n✓ Firmware flashed successfully!")
            print("\nThe gamepad may restart automatically.")
            print("If it doesn't, please manually restart it by disconnecting and reconnecting.")
            return True
        else:
            print(f"\n✗ Error flashing firmware (exit code: {result.returncode})")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error running fwupdtool: {e}")
        return False
    except FileNotFoundError:
        print("Error: fwupdtool not found. Please install fwupd.")
        return False


def print_instructions():
    """Print instructions for putting gamepad in bootloader mode"""
    print("\n" + "=" * 60)
    print("  INSTRUCTIONS")
    print("=" * 60)
    print("\n1. Put your gamepad in bootloader mode:")
    print("   - Hold down L1 + R1 + START for 3 seconds")
    print("   - A status LED should blink RED")
    print("\n2. Connect the gamepad to your computer via USB cable")
    print("\n3. Press Enter when ready...")
    print("=" * 60 + "\n")
    input()


def cleanup_firmware_file(filename):
    """Ask user if they want to keep the firmware file"""
    response = input(f"\nDo you want to keep the firmware file '{filename}'? (y/n): ").strip().lower()
    if response != 'y':
        try:
            os.remove(filename)
            print(f"✓ Removed {filename}")
        except OSError as e:
            print(f"Error removing file: {e}")


def main():
    """Main function"""
    print_header()
    
    # Check if fwupd tools are available
    try:
        subprocess.run(['fwupdmgr', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: fwupd is not installed or not in PATH.")
        print("Please install fwupd first: sudo apt install fwupd")
        sys.exit(1)
    
    # Step 1: Select gamepad
    display_gamepads()
    selected_gamepad = select_gamepad()
    print(f"\nSelected: {selected_gamepad['name']}")
    
    # Step 2: Fetch firmware list
    include_beta = input("\nInclude beta versions? (y/n): ").strip().lower() == 'y'
    firmware_list = fetch_firmware_list(selected_gamepad['type'], include_beta)
    
    if not firmware_list:
        print("Failed to fetch firmware list. Exiting.")
        sys.exit(1)
    
    # Step 3: Select firmware version
    firmware_list = display_firmware_versions(firmware_list)
    selected_firmware = select_firmware(firmware_list)
    
    if not selected_firmware:
        print("Exiting.")
        sys.exit(0)
    
    # Step 4: Download firmware
    firmware_file = download_firmware(selected_firmware)
    
    if not firmware_file:
        print("Failed to download firmware. Exiting.")
        sys.exit(1)
    
    # Step 5: Show instructions
    print_instructions()
    
    # Step 6: Get device ID
    device_id = get_gamepad_device_id()
    
    if not device_id:
        print("\nCouldn't find your gamepad. Make sure it's in bootloader mode and connected.")
        cleanup_firmware_file(firmware_file)
        sys.exit(1)
    
    # Step 7: Confirm before flashing
    response = input("\nProceed with firmware update? (y/n): ").strip().lower()
    if response != 'y':
        print("Update cancelled.")
        cleanup_firmware_file(firmware_file)
        sys.exit(0)
    
    # Step 8: Flash firmware
    success = flash_firmware(firmware_file, device_id)
    
    # Step 9: Cleanup
    cleanup_firmware_file(firmware_file)
    
    if success:
        print("\n" + "=" * 60)
        print("  Update completed successfully!")
        print("=" * 60 + "\n")
    else:
        print("\nUpdate failed. Please try again or update manually.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
