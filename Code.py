import numpy as np
import cv2
import time
import datetime
cap = cv2.VideoCapture('Location of video file else 1') #Open video file
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = True) #Create the background substractor
kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((11,11),np.uint8)
areaTH = 15000      #threshold area of contour, it could be changed accordingly
end1=0
start1=time.time()
l=0
file = open("Output.txt","w")   #opening file in write mode 
while(cap.isOpened()):
    ret, frame = cap.read() #read a frame
    
    fgmask = fgbg.apply(frame) #Use the substractor
    
    try:
        ret,imBin= cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        #Opening (erode->dilate) para quitar ruido.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate -> erode) para juntar regiones blancas.
        mask =  cv2.morphologyEx(mask , cv2.MORPH_CLOSE, kernelCl)
    except:
        #if there are no more frames to show...
        print('video ended')
        break

    _, contours0, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8) #drow contours
        area = cv2.contourArea(cnt)
        if area > areaTH:          #if the area of contour is grater than a particular threshold area
            start=time.time()               
            if(l==0):
                l=1
            if(l==1):
                start2=time.time()         #Saves the first entry time of on object in frame
                l=l+1
                file.write(str(datetime.timedelta(seconds=((start2//1)-(start1//1)))))  #writing in a file
                file.write("\t")
                
            x,y,w,h = cv2.boundingRect(cnt)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)  #Drawing rectangle about the object
            #cv2.imshow('Frame2',img)
        else:
            end=time.time()
            if(l==2):
                end1=time.time()            #saves the entry time if the tim gap is more than 5 secs
                if(end1-start>=5):
                    end2=time.time()
                    l=0
                    file.write(str(datetime.timedelta(seconds=((end2//1)-(start1//1)-5)))) #writing in a file
                    file.write("\n")
    cv2.resizeWindow('Frame',600,600)    
    cv2.imshow('Frame',frame)
    
    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break
cap.release() #release video file
cv2.destroyAllWindows()   #close all openCV windows
file.close()   #Closing file
