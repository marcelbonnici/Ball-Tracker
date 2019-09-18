import serial
import time

def main():
    ser=serial.Serial('/dev/ttyACM0')
    ser.write('\x84\x00\x1F\x00')
    ser.write('\x84\x01\x1F\x00')
    firstturn=0
    while firstturn < 90:
        firstturn=firstturn+1
        fus=(992+(int(firstturn)*11))*4
        fbin=''
        #sbin=''
        for i in range(0, 14):
            first=fus / 2
            frem=fus % 2
            fbin= str(frem)+ fbin
            fus=first
            #for j in range(0, 14):
            #    sec=sus / 2
            #    srem=sus % 2
            #    sbin= str(srem)+ sbin
            #    sus=sec
        p3=int('0'+ fbin[7:], 2)
        p4=int('0' + fbin[:7], 2)
        p3=int('0'+ fbin[7:], 2)
        p4=int('0' + fbin[:7], 2)

        #p5=int('0'+ sbin[7:], 2)
        #p6=int('0' + sbin[:7], 2)
        #p5=int('0'+ sbin[7:], 2)
        #p6=int('0' + sbin[:7], 2)

        # Courtesy of rjha94 on StackExchange: https://stackoverflow.com/questions/17589942/using-pyserial-to-send-binary-data
        packet=bytearray()
        packet.append(0x84)
        packet.append(0x00)
        packet.append(p3)
        packet.append(p4)
        ser.write(packet)
        time.sleep(.1)
        #spacket=bytearray()
        #spacket.append(0x84)
        #packet.append(0x01)
        #spacket.append(p5)
        #spacket.append(p6)
        #ser.write(spacket)
    ser.close()
if __name__ == '__main__':
    main()
