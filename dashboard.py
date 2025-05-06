import serial
import math
import time
import requests

# --- Serial Port Setup ---
port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

while True:
    try:
        statement = port.read(100)
        data = statement.decode(errors="ignore").split(",")

        if len(data) == 8:
            sensor_data = {
                "temperature": float(data[0].strip()),
                "humidity": float(data[1].strip()),
                "battery_voltage": float(data[2].strip()),
                "battery_performance": math.ceil(float(data[3].strip())),
                "latitude": float(data[4].strip()),
                "longitude": float(data[5].strip()),
                "wind_speed": float(data[6].strip()),
                "identifier": str(data[7].strip())
            }

            try:
                response = requests.post("http://127.0.0.1:8000/esp-data", json=sensor_data)
                response.raise_for_status()
                print("✅ Data sent successfully:", response.json())
            except requests.exceptions.RequestException as e:
                print("❌ Request failed:", e)

        time.sleep(1)

    except Exception as e:
        print(f"⚠️ Serial read error: {e}")
        time.sleep(1)
