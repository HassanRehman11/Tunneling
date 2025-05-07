import serial
import math
import time
import requests

# --- Wait for Serial Port to Open ---
while True:
    try:
        port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        print("✅ Serial port opened successfully.")
        break
    except serial.SerialException as e:
        print(f"⏳ Waiting for serial port: {e}")
        time.sleep(20)

# --- Main Loop ---
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
                headers = {
                    "accept": "application/json",
                    "x-api-key": "]H`+zZXUPLIo;,o2~~z5.EaDs]CV`K[0QtAZ'ziJ6,FUJ3BYnbC3.aH=0&6=aRS"
                }
                response = requests.post("http://esp32-lb-439368524.us-east-1.elb.amazonaws.com/esp-data", json=sensor_data, headers=headers)
                response.raise_for_status()
                print("✅ Data sent successfully:", response.json())
            except requests.exceptions.RequestException as e:
                print("❌ Request failed:", e)

    except Exception as e:
        print(f"⚠️ Serial read error: {e}")
        time.sleep(1)
