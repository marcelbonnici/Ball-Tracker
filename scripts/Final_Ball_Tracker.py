import cv2
import numpy as np
import serial #yummy serial
import time
cap = cv2.VideoCapture(2)

firstturn = 0 #degrees
secturn=0

ser=serial.Serial('/dev/ttyACM0')

def posc():
    global firstturn
    global secturn
    fus=(992+(int(firstturn)*11))*4
    sus=(992+(int(secturn)*11))*4
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
    #time.sleep(.1)

def main():
    global ser
    ser=serial.Serial('/dev/ttyACM0')

    xpos='\x84\x00\x1F\x00'
    ypos='\x84\x00\x1F\x00'
    ser.write(xpos)
    ser.write(ypos)
    ctrx=int(640/2)
    ctry=int(480/2)
    centerx=int(640/2)
    centery=int(480/2)

    while(1):
        # Take each frame
        _, frame = cap.read()
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of lime color in HSV
        lower_lime = np.array([10,68,214])
        upper_lime = np.array([38,252,255])

        # Threshold the HSV image to get only lime colors
        mask = cv2.inRange(hsv, lower_lime, upper_lime)

        #contouring coutesy of YouTuber Pysource's guidance
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

        #for loop coutesy of YouTuber Pysource's guidance
        for i in contours:
            (x, y, w, h) = cv2.boundingRect(i)

            ctrx = int((2*x+w)/2)
            ctry = int((2*y+h)/2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            break

        # Bitwise-AND mask and original image
        #res = cv2.bitwise_and(frame,frame, mask= mask)

        #vertical line coutesy of YouTuber Pysource's guidance
        cv2.line(frame, (ctrx, 0), (ctrx, 480), (0, 255, 0), 2)
        cv2.line(frame, (0, ctry), (640, ctry), (255, 0, 0), 2)

        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        #v2.imshow('res',res)
        k = cv2.waitKey(1)
        if k == 27:
            break
        global firstturn
        global secturn

        #if-elif inspired by YouTuber pysource
        if ctrx < centerx -30 and firstturn > 0:
            firstturn -=.5
        elif ctrx > centerx +30 and firstturn < 90:
            firstturn += .25
        if ctry < centery -30 and secturn > 0:
            secturn -=.5
        elif ctry > centery +30 and secturn < 90:
            secturn += .5
        posc()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
