import time
import serial
import datetime

# https://www.domoticaforum.eu/uploaded/Ard%20M/Opentherm%20Protocol%20v2-2.pdf

ser = serial.Serial('/dev/ttyUSB0', timeout = 1)
ser.isOpen()

while True:
    ser.write('PS=1'  + '\r')
    time.sleep(2)

    msg = ser.read(200)

    values = msg.split(',')

    now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

    if len(values) == 25: 
        item = (now       + ', ' + 
            values[6]     + ', ' + # Relative modulation level
            values[9]     + ', ' + # Boiler water temperature
            values[12]    + ', ' + # Return water temperature 
            values[0][22] + ', ' + # CH mode
            values[0][21] + ', ' + # DHW mode
            values[0][20] + ', ' + # Flame status
            values[0][23] + '\n' ) # Fault

        with open('/home/pi/otgw/log.txt', 'a') as file:
            file.write(item)

    #print out
    #print item
    time.sleep(10)
