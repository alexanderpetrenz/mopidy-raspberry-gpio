import logging

logger = logging.getLogger(__name__)


class RotEncoder:
    def __init__(self, rot_id):
        self.id = rot_id
        self.pins = []
        self.events = []
        self.state = (None, None)
        self.state_map = {
            ((False, False), (False, True)): 0,
            ((False, False), (True, False)): 1,
            ((False, True), (True, True)): 0,
            ((False, True), (False, False)): 1,
            ((True, False), (False, False)): 0,
            ((True, False), (True, True)): 1,
            ((True, True), (True, False)): 0,
            ((True, True), (False, True)): 1,
        }

    def add_pin(self, pin, event):
        if len(self.pins) == 2:
            raise RuntimeError(f"Too many pins for rotary encoder {self.id}!")

        self.pins.append(pin)
        self.events.append(event)
        logger.debug(f"Encoder{self.id}: Registered pin {pin}, event {event}")

    def get_state(self):
        import RPi.GPIO as GPIO

        level0 = GPIO.input(self.pins[0])
        level1 = GPIO.input(self.pins[1])

        return (level0, level1)

    def get_direction(self, current, new):
        return self.state_map[(current, new)]

    def get_event(self):
        next_state = self.get_state()

        event = None

        logger.debug(f"current state {self.state}")
        logger.debug(f"next state {next_state}")

        try:
            direction = self.get_direction(self.state, next_state)
            event = self.events[direction]
            logger.debug(f"retrieved direction {direction}, event {event}")
        except KeyError:
            logger.debug("KeyError occurred on retrieving direction and/or event")

        self.state = next_state
        return event
