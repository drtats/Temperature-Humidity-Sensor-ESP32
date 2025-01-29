import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime
from pathlib import Path

# ---------------- USER CONFIG ----------------
SERIAL_PORT = "/dev/cu.usbserial-0001"  # Change to your actual port on Mac
BAUD_RATE = 115200
PLOT_INTERVAL_MS = 1000  # Plot update interval (ms)

FOLDER_PATH = Path("Path/to/your/folder/to/save/csv")  # Where to save the CSV

# ---------------- GLOBAL STATE ---------------
time_data = []  # Stores elapsed time (seconds, normalized)
unix_timestamps = []  # Raw Unix timestamps
temp_data = []  # Stores temperature
hum_data = []  # Stores humidity

ser = None
csv_file = None

fig = None
ax = None
temp_line = None
hum_line = None


def open_serial_and_csv():
    """Open serial port and create a timestamped CSV file."""
    global ser, csv_file

    # Open serial port
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Allow ESP32 time to initialize

    # Create a timestamped CSV file
    now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = FOLDER_PATH / f"dht11_realtime_{now_str}.csv"
    csv_file = open(csv_filename, "w", encoding="utf-8")

    # Write CSV header
    csv_file.write("Timestamp (Unix),Time (s),Humidity (%),Temperature (C)\n")
    csv_file.flush()

    print(f"Logging data to {csv_filename} ... Press Ctrl+C to stop.")


def close_resources():
    """Close the CSV file and serial port if open."""
    global ser, csv_file
    if csv_file:
        csv_file.close()
    if ser:
        ser.close()
    print("Resources closed.")


def init_plot():
    """Initialize the Matplotlib plot."""
    global fig, ax, temp_line, hum_line

    fig, ax = plt.subplots()

    # Create line objects for temperature and humidity
    temp_line, = ax.plot([], [], 'r-', label="Temperature (°C)")
    hum_line, = ax.plot([], [], 'b-', label="Humidity (%)")

    # Set axis labels and legend
    ax.set_xlim(0, 10)  # X-axis range will expand dynamically
    ax.set_ylim(0, 100)  # Y-axis fixed for humidity and temperature
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.legend(loc="upper right")

    # Handle plot window close
    fig.canvas.mpl_connect("close_event", on_close)


def on_close(event):
    """Handle plot window close event."""
    close_resources()


def update_animation(frame):
    """Update function for FuncAnimation."""
    global ser, csv_file

    # Read a line from the serial port
    line = ser.readline().decode("utf-8", errors="replace").strip()
    if not line:
        return temp_line, hum_line  # Skip if no data is read

    # Parse the serial data: "humidity,temperature"
    parts = line.split(",")
    if len(parts) != 2:
        return temp_line, hum_line  # Skip invalid data

    try:
        humidity = float(parts[0])
        temperature = float(parts[1])
    except ValueError:
        return temp_line, hum_line  # Skip invalid numbers

    # Get current Unix timestamp
    current_unix_time = time.time()

    # Calculate elapsed time from the first timestamp
    if not unix_timestamps:  # First data point
        elapsed_time = 0
    else:
        elapsed_time = current_unix_time - unix_timestamps[0]

    # Append data to lists
    unix_timestamps.append(current_unix_time)
    time_data.append(elapsed_time)
    hum_data.append(humidity)
    temp_data.append(temperature)

    # Write to CSV
    csv_file.write(f"{current_unix_time},{elapsed_time},{humidity},{temperature}\n")
    csv_file.flush()

    # Print data to the terminal
    print(f"Time={elapsed_time:.1f}s  Hum={humidity:.2f}%  Temp={temperature:.2f}C")

    # Update plot lines
    temp_line.set_data(time_data, temp_data)
    hum_line.set_data(time_data, hum_data)

    # Dynamically adjust the x-axis
    if elapsed_time > ax.get_xlim()[1]:
        ax.set_xlim(0, elapsed_time + 5)

    return temp_line, hum_line


def main():
    try:
        # Open serial port and CSV file
        open_serial_and_csv()

        # Initialize the plot
        init_plot()

        # Start real-time animation
        ani = FuncAnimation(fig, update_animation, interval=PLOT_INTERVAL_MS, blit=False)

        # Display the plot (blocks until closed)
        plt.show()

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Closing resources.")
        close_resources()
    except Exception as e:
        print(f"Unhandled exception: {e}")
        close_resources()


if __name__ == "__main__":
    main()
