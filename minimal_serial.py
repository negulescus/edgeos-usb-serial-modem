import serial
import threading
import sys

def read_from_serial(ser):
    """Function to read data from the serial device."""
    try:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                sys.stdout.write(data)
                sys.stdout.flush()
    except Exception as e:
        print("\nError reading from serial:", e)
    finally:
        ser.close()

def main():
    serial_port = "/dev/ttyUSB0"
    baud_rate = 115200 # Adjust according to your device settings

    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        print(f"Connected to {serial_port} at {baud_rate} baud. Type AT commands below.")

        # Start the read thread
        read_thread = threading.Thread(target=read_from_serial, args=(ser,))
        read_thread.daemon = True
        read_thread.start()

        # Interactive send loop
        while True:
            try:
                user_input = raw_input("") + "\r\n"  # Add CRLF to the command
                ser.write(user_input)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    except serial.SerialException as e:
        print(f"Could not open serial port {serial_port}: {e}")
    except Exception as e:
        print("Unexpected error:", e)
    finally:
        ser.close()

if __name__ == "__main__":
    main()
