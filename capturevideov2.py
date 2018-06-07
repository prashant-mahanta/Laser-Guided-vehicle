import cv2
import urllib
from urllib.request import urlopen
import numpy as np
import serial
q={'l':0,'r':0,'f':0,'b':0,'s':0,'x':0}
hue_min=0
hue_max=120
sat_min=0
sat_max=200
val_min=200
val_max=256
cam_width=1250
cam_height=690
counter=0
#file="C:/Users/Sagar/Desktop/fcom/finally.txt"
ser = serial.Serial("COM11", 9600)
def threshold_image(channel,img):
        #choose channels in hue,saturation,value
        if channel == "h":
            minimum = hue_min
            maximum = hue_max
        elif channel == "s":
            minimum = sat_min
            maximum = sat_max
        elif channel == "v":
            minimum = val_min
            maximum = val_max
        (t,tmp)=cv2.threshold(
                img,    #src
                maximum,        #threshold value
                0,      #we don't care bacause of the selected type
                cv2.THRESH_TOZERO_INV   #t type
                )
        (t,img)=cv2.threshold(
                tmp,    #src
                minimum,        #threshold value
                255,    #maxvalue
                cv2.THRESH_BINARY       #type
                )
        if(channel=="h"):
                #only works for filtering red color because the range for the hue
                #is split
                img=cv2.bitwise_not(img)
        return img
def track(img,l):
        #RETR_EXTERNAL: retrieves only the extreme outer contours.
        #CHAIN_APPROX_SIMPLE: It removes all redundant points and compresses the contour.
        #                       represents contour with few points.saves memory.
        countours = cv2.findContours(l, cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)[-2]
        #only proceed if at least one contour was found
        if(len(countours)>0):
                #find the largest contour in the mask, then use
                #it to compute the minimum enclosing circle and
                #centroid
                c = max(countours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                #moments tell about center
                moments = cv2.moments(c)
                #Cx=m10/m00,Cy=m01/m00, m00=contour area
                if moments["m00"] > 0:
                        center = int(moments["m10"] / moments["m00"]), \
                                 int(moments["m01"] / moments["m00"])
                else:
                        center = int(x), int(y)
                        
                # only proceed if the radius meets a minimum size
                if(radius>10):
                        # print the center
                        #print(center)
                        x=center[0]
                        y=center[1]
                        #Move according to the pointer
                        #Upper part of screen
                        if((x>=310 and x<=900) and (y>=0 and y<=500)):
                                #print("move forward")
                                q['f']+=1
                        if((x>=310 and x<=900) and (y>=500 and y<=600)):
                                #print("stop")
                                q['s']+=1
                        elif(x>900):
                                #print("move right")
                                q['r']+=1
                        elif(x<310):
                                #print("move left")
                                q['l']+=1
                        #lower part
                        elif((x>=310 and x<=900) and (y>=600)):
                                #print("move back")
                                q['b']+=1
                        #cv2.circle(img, (int(x), int(y)), int(radius),
                           #(0, 255, 255), 2)
        else:
                #print("search")
                q['x']+=1
def create_and_position_window( name, xpos, ypos):
        """Creates a named widow placing it on the screen at (xpos, ypos)."""
        # Create a window
        cv2.namedWindow(name)
        # Resize it to the size of the camera image
        cv2.resizeWindow(name, cam_width, cam_height)
        # Move to (xpos,ypos) on the screen
        cv2.moveWindow(name, xpos, ypos)
while(1):
        url="http://192.168.43.1:8080/shot.jpg"
        counter+=1
        img=urlopen(url)
        #Create byte array of the image and store in numpy array
        imgnp=np.array(bytearray(img.read()),dtype=np.uint8)
        img=cv2.imdecode(imgnp,-1)
        #create_and_position_window('test',0,0)
        create_and_position_window('laser',0, 0)
        #cv2.imshow('test',img)
        hsv_img=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_img)
        #cv2.imshow('test2',h)
        #cv2.imshow('test3',s)
        #cv2.imshow('test4',v)
        h=threshold_image("h",h)
        s=threshold_image("s",s)
        v=threshold_image("v",v)
        #find bitwise AND of h and v and s
        l=cv2.bitwise_and(h,v)
        l=cv2.bitwise_and(s,l)
        
        hsv_image=cv2.merge([h,s,v])
        
        track(img,l)
        if(counter>=5):
                m='s'
                for key,values in q.items():
                        if(q[key]>q[m]):
                                m=key
                        q[key]=0
                print(m)
                ser.write(m.encode())
                #f=open(file,"w")
                #f.write(m)
                #f.close()
                counter=0
        cv2.imshow('laser',l)
        #exit key
        if(ord('q')==cv2.waitKey(10)):
                exit(0)
        
