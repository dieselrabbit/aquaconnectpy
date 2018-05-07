import time
from aquaconnectpy.controller import Controller

def getopts(argv):
    try:
        opts = {}  # Empty dictionary to store key-value pairs.
        while argv:  # While there are arguments left to parse...
            if argv[0][0:1] == '--':  # Found a "--name" arg.
                opts[argv[0][1:]] = True  # Add key and value to the dictionary.
            elif argv[0][0] == '-':  # Found a "-name value" pair.
                opts[argv[0][1:]] = argv[1]  # Add key and value to the dictionary.
            argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
        return opts
    except IndexError:
        print('Error, Malformed command args')
        sys.exit(2)
        
if __name__ == '__main__':
    import sys
    myargs = getopts(sys.argv)
    myargs['a'] = '192.168.1.15' # Debug
    #myargs['-p'] = True
    myargs['L'] = '5'
    myargs['i'] = '10'
    
    if 'a' in myargs:  # Example usage.
        print(myargs['a'])
    #print(myargs)

    try:
        address = myargs['a']
    except KeyError:
        print('Error, missing address')
        sys.exit(2)

    pool = Controller(address)

    if '-p' in myargs:
        pool.print_panel()
    elif 'l' in myargs:
        led = int(myargs["l"])
        if 'i' in myargs:
            interval = int(myargs['i'])
            while KeyboardInterrupt:
                pool.update()
                print(pool.sensors[led].get_state())
                time.sleep(interval)
        else:
            print(pool.sensors[led].get_state())
    elif 'L' in myargs:
        led = int(myargs["L"])
        if 'i' in myargs:
            interval = int(myargs['i'])
            while KeyboardInterrupt:
                pool.update()
                print(pool.sensors[led].get_label(), '=', pool.sensors[led].get_state())
                time.sleep(interval)
        else:
            print(pool.sensors[led].get_label(), '=', pool.sensors[led].get_state())
    elif 's' in myargs:
        switch = int(myargs["s"])
        print(myargs['toggle'])
        pool.switches[switch].toggle()
