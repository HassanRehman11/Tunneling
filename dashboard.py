import streamlit as st
import serial
import math
import time
import requests
# --- Serial Port Setup ---
port = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# --- Streamlit Config ---
st.set_page_config("Unit Live Dashboard", layout="wide")
st.title("📡 Unit Live Sensor Dashboard")

# --- Containers ---
placeholder = st.empty()
chart_placeholder = st.empty()

# --- History Buffers ---
temperature_data = []
humidity_data = []
voltage_data = []
performance_data = []
time_labels = []

# --- Main Loop ---
while True:
    try:
        statement = port.read(100)
        data = statement.decode(errors="ignore").split(",")

        if len(data) == 7:
            st.title(f"📡 {str(data[7].strip())} Live Sensor Dashboard")
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
                print("Server response:", response.json())
            except requests.exceptions.RequestException as e:
                print("Request failed:", e)

            # Update buffers
            timestamp = time.strftime("%H:%M:%S")
            temperature_data.append(sensor_data["temperature"])
            humidity_data.append(sensor_data["humidity"])
            voltage_data.append(sensor_data["battery_voltage"])
            performance_data.append(sensor_data["battery_performance"])
            time_labels.append(timestamp)

            # Keep last 20 entries
            max_len = 20
            temperature_data = temperature_data[-max_len:]
            humidity_data = humidity_data[-max_len:]
            voltage_data = voltage_data[-max_len:]
            performance_data = performance_data[-max_len:]
            time_labels = time_labels[-max_len:]

            # --- Metrics ---
            with placeholder.container():
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🌡 Temperature", f"{sensor_data['temperature']} °C")
                col2.metric("💧 Humidity", f"{sensor_data['humidity']} %")
                col3.metric("🔋 Voltage", f"{sensor_data['battery_voltage']} V")
                col4.metric("⚡ Battery %", f"{sensor_data['battery_performance']} %")

                col5, col6, col7 = st.columns(3)
                col5.metric("🌍 Latitude", f"{sensor_data['latitude']}")
                col6.metric("🌍 Longitude", f"{sensor_data['longitude']}")
                col7.metric("💨 Wind Speed", f"{sensor_data['wind_speed']} km/h")

                st.subheader("📍 Live Location")
                map_df = pd.DataFrame([{
                    "lat": sensor_data["latitude"],
                    "lon": sensor_data["longitude"]
                }])
                st.map(map_df, zoom=15)

            # --- Line Charts ---
            with chart_placeholder.container():
                st.subheader("📈 Live Sensor Trends")
                chart_df = pd.DataFrame({
                    "Temperature (°C)": temperature_data,
                    "Humidity (%)": humidity_data,
                    "Voltage (V)": voltage_data,
                    "Battery %": performance_data
                }, index=time_labels)

                st.line_chart(chart_df)

        time.sleep(1)

    except Exception as e:
        st.error(f"Error reading from serial: {e}")
        time.sleep(1)
