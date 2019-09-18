import serial


def main():
    ser=serial.Serial('/dev/ttyACM0')
    #ser.write statement courtesy of Northwestern MSR student Michael Doody's assistance
    ser.write('\x84\x00\x1F\x00')
    ser.write('\x84\x01\x1F\x00')
    #print('\x84\x00\x1F\x00')
    firstturn= raw_input( 'List the degree rotation of the base (between 0 and 90): ')
    secturn= raw_input( 'List the degree rotation of the head (between 0 and 90): ')
    sus=(992+(int(secturn)*11))*4
    fus=(992+(int(firstturn)*11))*4
    fbin=''
    sbin=''
    for i in range(0, 14):
        first=fus / 2
        frem=fus % 2
        fbin= str(frem)+ fbin
        fus=first
    for j in range(0, 14):
        sec=sus / 2
        srem=sus % 2
        sbin= str(srem)+ sbin
        sus=sec
    p3=int('0'+ fbin[7:], 2)
    p4=int('0' + fbin[:7], 2)
    p3=int('0'+ fbin[7:], 2)
    p4=int('0' + fbin[:7], 2)

    p5=int('0'+ sbin[7:], 2)
    p6=int('0' + sbin[:7], 2)
    p5=int('0'+ sbin[7:], 2)
    p6=int('0' + sbin[:7], 2)

    # Courtesy of rjha94 on StackExchange: https://stackoverflow.com/questions/17589942/using-pyserial-to-send-binary-data
    packet=bytearray()
    packet.append(0x84)
    packet.append(0x00)
    packet.append(p3)
    packet.append(p4)
    ser.write(packet)

    spacket=bytearray()
    spacket.append(0x84)
    spacket.append(0x01)
    spacket.append(p5)
    spacket.append(p6)
    ser.write(spacket)
    ser.close()

#if statement courtesy of Northwestern MSR student Michael Doody's assistance
if __name__ == '__main__':
    main()

"""
import serial
ser=serial.Serial('/dev/ttyACM0')
print(ser.name)
ser.write('\x84\x00\x58\x36')
ser.write('\x84\x01\x58\x36')
ser.close()

70 2E
58 36
"""

#0110110 1011000
#0x36    58
