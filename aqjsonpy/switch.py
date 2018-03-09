from aqjsonpy.device import AQDevice

class AQSwitch(AQDevice):
    def __init__(self, data, controller):
        super().__init__(data, controller)
        self.key_id = data['key_id']
      
    def hass_state(self):
        if self.__state == 'on' or self.__state == 'blink':
            return 'on'
        else:
            return 'off'

    def toggle(self):
        self._AQDevice__controller.toggle_switch(self, self.key_id)
