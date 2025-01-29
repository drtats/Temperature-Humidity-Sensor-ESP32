# ESP32 DHT11 Temperature & Humidity Logger

## 📖 Overview

This project logs **temperature and humidity** data from a **DHT11 sensor** using an **ESP32**.  
Users can choose between:
- **🔌 Wired Mode** (USB Serial)
- **📡 Wireless Mode** (Bluetooth Serial)

The data is **logged in real time**, saved as a **CSV file**, and optionally **plotted live** using Python.

---


## 🛠️ Hardware Requirements
- **ESP32** (any model with Bluetooth)
- **DHT11** or **DHT22** Temperature & Humidity Sensor
- USB cable (for wired mode)

---


## 💾 Installation & Setup

### **1️⃣ Flash the ESP32**
1. Install **Arduino IDE** and the **ESP32 board package**.
2. Install the required Arduino libraries:
   - **DHT sensor library** (`DHT.h`)
   - **Bluetooth Serial library** (`BluetoothSerial.h`) *(for Bluetooth mode)*
3. Upload the appropriate **Arduino sketch**:
   - **`DHT11_temperature_humidity_measurement.ino`** → For **USB Serial**
   - **`DHT11_temperature_humidity_measurement_bluetooth.ino`** → For **Bluetooth Serial**

---

### **2️⃣ Run the Python Logger**
1. Install **Python 3** and the required libraries:
    ```bash
    pip install pyserial matplotlib
    ```
2. Choose the correct script:
  - **For USB Serial:**
    ```bash
    python Python/Humidity_Temperature_ESP32.py
    ```
  - **For Bluetooth Serial:**
    ```bash
    python Python/Humidity_Temperature_ESP32_Bluetooth.py
    ```
3. Specify the **folder path** to save the CSV file in a code.


The script will:
Log data to a CSV file (saved automatically).
Display real-time temperature & humidity in the terminal.
Plot live data (if enabled).


# 📂 Repository Structure
```graphql
ESP32_DHT11_Logger/
│── Arduino/
│   ├── DHT11_temperature_humidity_measurement.ino         # USB Serial version
│   ├── DHT11_temperature_humidity_measurement_bluetooth.ino     # Bluetooth Serial version
│
│── Python/
│   ├── Humidity_Temperature_ESP32.py         # USB Serial data logger
│   ├── Humidity_Temperature_ESP32_Bluetooth.py     # Bluetooth data logger
```


# ⚡ Example Output
Terminal Output (USB or Bluetooth)
```plaintext
Time=0.0s  Hum=45.3%  Temp=23.7°C
Time=1.0s  Hum=46.2%  Temp=24.0°C
```
CSV File (dht11_log_YYYYMMDD.csv)
```csv
Timestamp (Unix),Time (s),Humidity (%),Temperature (C)
1738087160.1,0.0,45.3,23.7
1738087161.1,1.0,46.2,24.0
```


## 🔗 Additional Notes
- **USB Mode**: Requires the correct **serial port** (`/dev/cu.usbserial-*` or `COM*`).
- **Bluetooth Mode**: Pair **ESP32** as `"ESP32_DHT11"`, then check `/dev/cu.*` for the correct port.

Plotting Issues? If the real-time plot doesn't appear, try running:
```bash
python -m pip install --upgrade matplotlib
```


# 🤝 Contributing
Pull requests and suggestions are welcome!
Feel free to fork this repo and improve the code.




