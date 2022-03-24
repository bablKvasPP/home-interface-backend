from time import sleep

from gpiozero import TonalBuzzer

from settings import BUZZER_PIN


class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        self.tone_buzzer = TonalBuzzer(BUZZER_PIN)

    def alert(self):
        self.tone_buzzer.play("A4")

    def silence(self):
        self.tone_buzzer.stop()


if __name__ == '__main__':
    from hardware_components import hardware

    hardware.initialize()
    hardware.buzzer.alert()
    sleep(1)
    hardware.buzzer.silence()
