import serial

if __name__ == "__main__":
    print("Start")
    while 1:
        try:
            with serial.Serial('/dev/ttyACM1', 115200) as ser:
                x = ser.read()
                print(int.from_bytes(x))
        except serial.serialutil.SerialException:
            pass