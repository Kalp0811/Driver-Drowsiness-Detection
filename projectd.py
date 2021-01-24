import numpy as np
import cv2
import playsound 
import argparse
from threading import Thread


def soundAlarm(path='C:/Users/srika/Desktop/DS/alarm.wav'):
	playsound.playsound(path)


counter=0
ALARM_ON = False
faceCascade = cv2.CascadeClassifier('C:/Users/srika/Desktop/DS/face.xml')
eyeCascade = cv2.CascadeClassifier('C:/Users/srika/Desktop/DS/eye.xml')
cap = cv2.VideoCapture(0) # vedio capturing
cap.set(3,640) # set Width
cap.set(4,480) # set Height


ap=argparse.ArgumentParser()
ap.add_argument("-a","--alarm",type=str,default="",help="C:/Users/srika/Desktop/DS/alarm.wav")
args=vars(ap.parse_args())


while(True):
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,scaleFactor = 1.2,minNeighbors=5,minSize = (20,20))
    
    for(x,y,w,h) in faces:
    	cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    	roi_gray = gray[y:y+h,x:x+w]
    	roi_color = frame[y:y+h,x:x+w]
    	ALARM_ON = False
    	eyes = eyeCascade.detectMultiScale(roi_gray,scaleFactor = 1.5,minNeighbors = 10,minSize = (5,5),)
    	if np.array(eyes).any() : 
    		counter=0
    		ALARM_ON=False
    		cv2.putText(frame, str(counter) , (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,251), 3, cv2.LINE_AA)
    	else :
    		counter+=1
    		cv2.putText(frame, str(counter) , (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,251), 3, cv2.LINE_AA)
    		if(counter>30):
    			cv2.putText(frame, "  Drowsiness alert" , (0,50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3, cv2.LINE_AA)
    			if not ALARM_ON:
    				ALARM_ON = True
    				
    				if args["alarm"]!="":
    					t=Thread(target = soundAlarm,args=(args["alarm"],))
    					t.deamon = True
    					t.start()	
    		
    
    	for(ex,ey,ew,eh) in eyes:
    		cv2.rectangle(roi_color,(ex,ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    
    	cv2.imshow('frame', frame)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
cap.release()
cv2.destroyAllWindows()
