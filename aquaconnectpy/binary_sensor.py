from aqjsonpy.device import AQDevice

class AQBinarySensor(AQDevice):
    def __init__(self, data, controller):
        super().__init__(data, controller)

    def hass_state(self):
        if self.__state == 'on' or self.__state == 'blink':
            return 'true'
        else:
            return 'false'

