class Buzzer:
    def __init__(self, pin):
        self.pin = pin

    def alert(self):
        GPIO.output(self.pin, 1)

    def silence(self):
        GPIO.output(self.pin, 0)
