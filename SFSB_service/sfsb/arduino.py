import serial


class Arduino:
    def __init__(self, port, baudrate=9600):
        self.arduino = serial.Serial(port=port, baudrate=baudrate)

    def send(self, msg: str):
        while not self.arduino.writable():
            pass
        self.arduino.write(msg.encode())

    def send_bytes(self, msg: bytes):
        while not self.arduino.writable():
            pass
        self.arduino.write(msg)

    def recv(self):
        if self.arduino.readable():
            return self.arduino.readall()
        return None

    def close(self):
        self.arduino.close()


class SFSBClient(Arduino):
    def led_on(self):
        self.send_bytes(bytes([1, 0]))

    def led_off(self):
        self.send_bytes(bytes([2, 0]))

    def motor_set_speed(self, speed):
        self.send_bytes(bytes([3, speed]))
