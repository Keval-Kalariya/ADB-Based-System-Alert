import subprocess
import time
import psutil
import platform

# ================= CONFIGURATION =================
ALERT_CPU_PERCENT = 1
ALERT_MEMORY_PERCENT = 1
ALERT_DISK_PERCENT = 1
CLIENT_PHONE = "919427389535"

ADB_PATH = r"C:\Users\keval\Downloads\adb\adb.exe"
# =================================================


def run_adb(*args, timeout=10):
    result = subprocess.run(
        [ADB_PATH, *args],
        capture_output=True, text=True, timeout=timeout
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_device_connected():
    rc, out, _ = run_adb("devices")
    lines = [l for l in out.splitlines() if "\tdevice" in l]
    return len(lines) > 0


def escape_for_adb(text):
    """
    Properly escape text for adb shell input text.
    - Spaces        → %s
    - Colons        → \\:   (colon breaks shell parsing)
    - Percent signs → \\%   (percent triggers URL encoding)
    - Ampersands    → \\&
    - Parentheses   → \\( \\)
    """
    result = ""
    for ch in text:
        if ch == " ":
            result += "%s"
        elif ch in r'\:%;()&<>|"\'`$!#':
            result += "\\" + ch
        else:
            result += ch
    return result


def send_sms(phone, message):
    if not check_device_connected():
        print("ERROR: No ADB device connected.")
        return False

    print(f"Preparing to send: {message}")

    # Step 1: Wake screen
    run_adb("shell", "input", "keyevent", "KEYCODE_WAKEUP")
    time.sleep(1)

    # Step 2: Open SMS app with pre-filled message body
    # This avoids focus issues and the need for manual typing/clearing.
    # We escape double quotes for the Android shell.
    safe_message = message.replace('"', '\\"')
    rc, _, err = run_adb(
        "shell", "am", "start",
        "-a", "android.intent.action.SENDTO",
        "-d", f"sms:{phone}",
        "--es", "sms_body", f"\"{safe_message}\"",
        "--ez", "exit_on_sent", "true"
    )
    if rc != 0:
        print(f"Failed to launch SMS app: {err}")
        return False

    time.sleep(2)  # Wait for app to load message

    # Step 3: Tap the Send button
    # Based on window_dump.xml, the send button is at [611,1491][706,1536]
    # We use the center point (658, 1513)
    run_adb("shell", "input", "tap", "658", "1513")
    time.sleep(1)

    print(f"SMS sent to {phone}")
    return True


def check_system():
    psutil.cpu_percent(interval=1)  # Warm-up call
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    host = platform.node()

    alerts = []
    if cpu > ALERT_CPU_PERCENT:
        alerts.append(f"CPU {cpu:.1f}pct")
    if mem.percent > ALERT_MEMORY_PERCENT:
        alerts.append(f"MEM {mem.percent:.1f}pct")
    if disk.percent > ALERT_DISK_PERCENT:
        alerts.append(f"DISK {disk.percent:.1f}pct")

    if alerts:
        # Use "pct" instead of "%" — percent sign breaks adb input text
        summary = ", ".join(alerts)
        message = f"ALERT on {host} - {summary} exceeded limit"
        send_sms(CLIENT_PHONE, message)
    else:
        print("System OK — no alerts.")


if __name__ == "__main__":
    # How often to check the system (in seconds)
    CHECK_INTERVAL = 300  # 300 seconds = 5 minutes

    print(
        f"Starting system monitor. Checking every {CHECK_INTERVAL} seconds...")
    print("Press Ctrl+C to stop if running in a terminal.")

    while True:
        try:
            check_system()
        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait before checking again
        time.sleep(CHECK_INTERVAL)
