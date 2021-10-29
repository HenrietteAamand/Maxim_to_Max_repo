import serial
import time
port = serial.Serial('COM17', baudrate=115200, timeout=3.0)
port.flushInput()
port.flushOutput()
port.write("stop\n".encode())
time.sleep(1)
#port.write("reset\n".encode())

print("done")
port.close()
