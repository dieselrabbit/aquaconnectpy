class AQDevice:
    def __init__(self, data, controller):
        self.__controller = controller
        self.__led_id = data['led_id']
        self.__label = data['label']
        self.__state = 'off'

    def set_state(self, state):
        self.__state = state

    def get_state(self):
        return self.__state

    def hass_state(self):
        if self.__state == 'on' or self.__state == 'blink':
            return 'true'
        else:
            return 'false'

    def get_label(self):
        return self.__label

    def get_id(self):
        return self.__led_id
