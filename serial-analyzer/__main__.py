import serial

if __name__ == "__main__":
    while 1:
        try:
            with serial.Serial('/dev/ttyACM1', 115200, timeout=1) as ser:
                x = ser.read()
                print(x)
        except serial.serialutil.SerialException:
            pass