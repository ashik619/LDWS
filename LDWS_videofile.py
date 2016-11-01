 from __future__ import division
import numpy as np
import cv2
import math
font = cv2.FONT_HERSHEY_SIMPLEX
mp=7
cap = cv2.VideoCapture("F:/ab.mp4")
while(cap.isOpened()):
    ret, frame = cap.read()
    frm1 = frame[120:238,1:425]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame',gray)
    src2 = gray[120:238,1:425]
    src= cv2.medianBlur(src2,3)
    dst = cv2.Canny(src, 70, 250)
    lines = cv2.HoughLines(dst, 1, math.pi/180.0, 85, np.array([]), 0, 0)
    try :
         a,b,c = lines.shape
    except AttributeError :
        continue
    p1=np.array([])
    #p2=np.array([])
    #p3=np.array([[1,1]])
    #p4=np.array([[1,1]])
    #p5=np.array([[1,1]])
    for i in range(a):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0, y0 = a*rho, b*rho
        pt1 = ( int(x0+1000*(-b)), int(y0+1000*(a)) )
        pt2 = ( int(x0-1000*(-b)), int(y0-1000*(a)) )
        if pt2[0]==pt1[0]:
            xi=pt2[0]
        elif pt2[1]==pt1[1]:
            xi=0
        else :
            m=((pt2[1]-pt1[1])/(pt2[0]-pt1[0]))
            b=pt2[1]-m*pt2[0]
            x=((118-b)/m)
            xi=math.floor(x)
            #y=m*x+b
        if 0 < xi < 400:
            p1=np.append(p1,xi)
        #p2=np.append(p2,pt2[0])
        #p3=np.vstack((p3,[pt1[0],pt1[1]]))
        #p4=np.vstack((p4,[pt2[0],pt2[1]]))
        #p5=np.vstack((p5,[x,y]))
        cv2.line(frm1, pt1, pt2, (0, 0, 255), 1, cv2.LINE_AA)
    p1=sorted(p1)
    if len(p1)!=0:
        m=np.mean(p1)
    else :
        m=0
    print 'p1',p1
    print 'mean',m
    if m!=0:
        if m > mp+17 :
            cv2.putText(frm1,'LEFT',(10,50), font, 2,(0,255,0),2,cv2.LINE_AA)
            mp=m
        elif m < mp-17 :
              cv2.putText(frm1,'RIGHT',(250,50), font, 2,(0,255,0),2,cv2.LINE_AA)
              mp=m        
    #print 'p3',p3
    #print 'p4',p4
    #print 'p5',p5
    cv2.imshow('frame',frm1)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

    
