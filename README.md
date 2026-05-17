# 📱 ADB-Based System Alert

> A Python automation tool that monitors your PC's system health (CPU, Memory, Disk) and sends **real-time SMS alerts** to a mobile phone via ADB (Android Debug Bridge) — no third-party SMS gateway required.

---

## 🧠 How It Works

The script runs a continuous monitoring loop on your Windows PC. Every 5 minutes, it checks the system's CPU, memory, and disk usage. If any metric exceeds a configured threshold, it automatically:

1. Wakes up your connected Android phone via ADB
2. Launches the default SMS app pre-filled with the alert message
3. Taps the **Send** button to deliver the SMS instantly

No internet-based notification service is needed — it uses your phone's native messaging app directly.

---

## ✨ Features

- 🔍 **Real-time system monitoring** — CPU, RAM, and Disk usage via `psutil`
- 📲 **SMS alerts via ADB** — Sends SMS directly through the connected Android phone
- 🔁 **Configurable thresholds** — Set your own alert limits for each metric
- 🧱 **No cloud dependency** — Works fully offline using USB + ADB
- 🔐 **Safe text escaping** — Handles special characters in ADB shell commands
- 🔄 **Auto-reconnect aware** — Checks device connection before every send attempt

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core scripting language |
| `psutil` | System resource monitoring |
| `platform` | Get the hostname of the PC |
| `subprocess` | Execute ADB shell commands |
| ADB (Android Debug Bridge) | Control Android phone over USB |

---

## 📁 Project Structure

```
adb/
├── system_alert.py        # Main monitoring & alert script
├── adb.exe                # ADB binary (Windows)
├── AdbWinApi.dll          # ADB Windows API library
├── AdbWinUsbApi.dll       # ADB USB API library
├── window_dump.xml        # UI dump used to locate Send button coordinates
├── fastboot.exe           # Fastboot utility (bundled with ADB)
└── README.md              # Project documentation
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Windows PC
- Python 3.8+
- An Android phone with **USB Debugging enabled**
- USB cable to connect the phone to the PC

### 1. Clone the Repository

```bash
git clone https://github.com/Keval-Kalariya/ADB-Based-System-Alert.git
cd ADB-Based-System-Alert
```

### 2. Install Python Dependencies

```bash
pip install psutil
```

### 3. Enable USB Debugging on Android

1. Go to **Settings → About Phone**
2. Tap **Build Number** 7 times to unlock Developer Options
3. Go to **Settings → Developer Options**
4. Enable **USB Debugging**
5. Connect your phone via USB and **Allow** the ADB connection prompt

### 4. Configure the Script

Open `system_alert.py` and update the configuration section at the top:

```python
# ================= CONFIGURATION =================
ALERT_CPU_PERCENT    = 80    # Alert if CPU usage exceeds 80%
ALERT_MEMORY_PERCENT = 85    # Alert if Memory usage exceeds 85%
ALERT_DISK_PERCENT   = 90    # Alert if Disk usage exceeds 90%
CLIENT_PHONE         = "91XXXXXXXXXX"  # Recipient phone number (with country code)

ADB_PATH = r"C:\path\to\your\adb.exe"  # Full path to adb.exe
# =================================================
```

> **Note:** The default thresholds are set to `1%` for testing purposes. Change them to realistic values (e.g., `80`, `85`, `90`) before production use.

### 5. Run the Script

```bash
python system_alert.py
```

The script will start monitoring and print status updates to the console every 5 minutes.

---

## 📲 SMS Alert Format

When a threshold is exceeded, the SMS sent to the phone looks like:

```
ALERT on DESKTOP-XXXXX - CPU 92.3pct, MEM 87.1pct exceeded limit
```

---

## 🔧 Customizing the Check Interval

The monitoring interval is set to **300 seconds (5 minutes)** by default. You can change this in the `__main__` block:

```python
CHECK_INTERVAL = 300  # Change to any value in seconds
```

---

## ⚠️ Known Limitations

- **Coordinate-based tapping**: The Send button is tapped using fixed screen coordinates (`658, 1513`) derived from `window_dump.xml`. These coordinates may differ on phones with different screen resolutions or SMS apps. Re-dump the UI layout with `adb shell uiautomator dump` if the button tap fails.
- **Single device support**: Currently works with one connected ADB device at a time.
- **Windows only**: The bundled `adb.exe` is for Windows. Linux/macOS users should use their system's ADB binary.

---

## 🧪 Testing the Setup

To verify ADB is working correctly before running the script:

```bash
# Check if ADB detects the device
adb devices

# Wake the screen
adb shell input keyevent KEYCODE_WAKEUP
```

---

## 📄 License

This project is licensed for personal and educational use. The bundled ADB binaries are owned by Google and are subject to the Android Open Source Project license. See [`NOTICE.txt`](NOTICE.txt) for details.

---

## 👨‍💻 Author

**Keval Kalariya**  
[GitHub](https://github.com/Keval-Kalariya) · Built with Python & ADB