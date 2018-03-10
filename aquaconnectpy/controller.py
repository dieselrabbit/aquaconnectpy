from urllib import parse, request
import binascii
import html
import time
from bs4 import BeautifulSoup
from aquaconnectpy.switch import AQSwitch
from aquaconnectpy.binary_sensor import AQBinarySensor

class Controller:
    def __init__(self, base_address, update_interval):
        self.__base_address = base_address
        self.update_interval = update_interval
        self.__message_lines = []
        self.__data_site = '/WNewSt.htm'
        self.__element_data = {}
        self.switches = {}
        self.sensors = {}

        self.setup()

        self.update()


    def setup(self):
        url = 'http://' + self.__base_address + '/'
        mappingSoup = self.__get_page_soup(url)
        tags = mappingSoup.select('td[id^="Key_"]')

        for tag in tags:
            tag_data = self.__parse_element(tag)
            self.__element_data[tag_data['led_id']] = tag_data
#            print(tag_data)

            if tag_data['key_id'] == '00':
                continue

            if tag_data['key_id'] != 'xx':
                self.switches[tag_data['led_id']] = AQSwitch(tag_data, self)
                
            self.sensors[tag_data['led_id']] = AQBinarySensor(tag_data, self)
            
        print('Controller setup.')

    def update(self, reqData=None):
        url = 'http://' + self.__base_address + self.__data_site
        urlRequest = request.Request(url, reqData, method='POST')
        dataSoup = self.__get_page_soup(urlRequest)

        lines = [x.strip("\r\n").strip()
                 for x in dataSoup.body.text.split('xxx')]
        self.__message_lines = [lines[0], lines[1]]
        bHex = binascii.hexlify(lines[2].encode())
        strLEDs = bHex.decode("utf-8")
        print(strLEDs)

        for i, v in enumerate(strLEDs):
            state = self.__map_led_state(v)
            if state == 'no_key':
                continue

            if i < len(strLEDs) - 1:
                self.switches[i].set_state(state)

            self.sensors[i].set_state(state)
                
        print('Status updated!')

        print(self.status_lines())
        #print(self.__message_lines[1])

        for led_id in sorted(self.sensors.keys()):
            print(led_id,
                  self.sensors[led_id].get_state(),
                  self.sensors[led_id].get_label())
            
        for led_id in sorted(self.switches.keys()):
            print(led_id,
                  self.switches[led_id].key_id,
                  self.switches[led_id].get_state(),
                  self.switches[led_id].get_label())


    def status_lines(self, line_num=None):
        if line_num in range(2):
            return self.__message_lines[line_num]
        else:
            return self.__message_lines[0] + '\n' + self.__message_lines[1]

    def toggle_switch(self, switch, key_id):
        pair = 'KeyId', key_id
        d = pair,
        Data = parse.urlencode(d)
        print(Data)
        bData = Data.encode('utf-8')
        url = 'http://' + self.__base_address + self.__data_site
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Content-length": len(bData),
                   "Connection": "close",
                   "Accept": "*/*\\"} # <- This is the key to it working
        urlRequest = request.Request(url, bData, headers)
        print(urlRequest.get_full_url(), bData)
        self.__get_page_soup(urlRequest)
        time.sleep(0.5)
        self.update()

    def __get_page_soup(self, url):
        response = request.urlopen(url)
        strData = response.read().decode('utf-8')
        response.close()
        #print(response.status, response.headers, strData)
        # default html parser seems to have trouble with escaped symbols
        return BeautifulSoup(html.unescape(strData), 'html.parser')

    def __map_led_state(self, state_num):
        '''Set the LED state from the number code'''
        if state_num == "3":
            return "no_key"
        elif state_num == "4":
            return "off"
        elif state_num == "5":
            return "on"
        elif state_num == "6":
            return "blink"
        else:
            return "no_key"

    def __parse_element(self, tag):
        data = {}
        #Parses the LED index associated with this tag
        prefix = 'Key_'
        dataLen = 2
        start = len(prefix)
        end = start + dataLen
        data['led_id'] = int(tag['id'][start:end])

        #Parses the 'key_id' for sending keypress commands
        prefix = 'WebsProcessKey("'
        dataLen = 2
        start = len(prefix)
        end = start + dataLen
        data['key_id'] =  tag['onclick'][start:end]

        #Gets the label for this tag if set by the pool controler
        if data['key_id'] == 'xx':
            data['label'] = 'CHECK SYSTEM'
        else:
            data['label'] = tag.text.strip()

        return data
        

        
    
