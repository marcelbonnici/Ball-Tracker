import cv2
import numpy as np
import serial #yummy serial
cap = cv2.VideoCapture(2)

def main():
    ser=serial.Serial('/dev/ttyACM0')
    #ser.write statement courtesy of Northwestern MSR student Michael Doody's assistance
    xpos='\x84\x00\x1F\x00'
    ypos='\x84\x00\x1F\x00'

    ##pwm = PCA9685(0x40, debug=False)
    ##pwm.setPWMFreq(50)
    ##pwm.setServoPosition(0, 90)
    ##cap=cv2.VideoCapture(2)
    _, frame = cap.read()
    rows, cols, _ = frame.shape
    ctrx=int(cols/2)
    ##position = 0 #degrees
    center=int(cols/2)

    while(1):
        ser.write(xpos)
        ser.write(ypos)
        # Take each frame
        _, frame = cap.read()
        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of lime color in HSV
        lower_lime = np.array([10,68,214])
        upper_lime = np.array([37,252,255])

        # Threshold the HSV image to get only lime colors
        mask = cv2.inRange(hsv, lower_lime, upper_lime)

        #contouring coutesy of YouTuber Pysource's guidance
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse=True)

        #for loop coutesy of YouTuber Pysource's guidance
        for i in contours:
            (x, y, w, h) = cv2.boundingRect(i)

            ctrx = int((2*x+w)/2) # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            ctry = int((2*y+w)/2)
            break

        # Bitwise-AND mask and original image
        #res = cv2.bitwise_and(frame,frame, mask= mask)

        #vertical line coutesy of YouTuber Pysource's guidance
        cv2.line(frame, (ctrx, 0), (ctrx, 480), (0, 0, 255), 2)
        cv2.line(frame, (0, ctry), (640, ctry), (0, 0, 255), 2)

        cv2.imshow('frame',frame)
        #cv2.imshow('mask',mask)
        #v2.imshow('res',res)
        k = cv2.waitKey(1)
        if k == 27:
            break

        ##if ctrx < center:
            ##position +=1
        ##elif ctrx > center:
            ##position -= 1
        ##pwm.setServoPosition(0, position)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
