import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot
cap =cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,360)
detection = FaceMeshDetector(maxFaces=1)

plotY= LivePlot(640,360,[20,50],invert=True)
ratiolist=[]

idList=[22,23,24,26,110,157,158,159,160,161,130,243,25,173]
blinkcount=0
counter=0
color=(0,255,0)
while True:
    check, frames = cap.read()
    check, faces= detection.findFaceMesh(frames,draw=False)

    if faces:
        face = faces[0]
        for id in idList:
            cv2.circle(frames,face[id],5,(255,0,0),cv2.FILLED)

        leftup=face[159]
        leftdown=face[23]
        leftleft=face[130]
        leftright=face[243]
        lenVer,_ = detection.findDistance(leftup,leftdown)
        lenhor,_ = detection.findDistance(leftleft,leftright)

        cv2.line(frames,leftleft,leftright,(0,0,255),3)
        cv2.line(frames,leftup,leftdown,(0,0,255),3)
        ratio = int((lenVer/lenhor)*100)
        ratiolist.append(ratio)
        if len(ratiolist)>3:
            ratiolist.pop(0)
        ratioAvg =sum(ratiolist)/len(ratiolist)

        if ratioAvg<35 and counter==0:
            blinkcount+=1
            color=(0,200,0)
            counter =1
        if counter!=0:
            counter+=1
            if counter>10:
                counter=0
                color=(255,0,255)
        cvzone.putTextRect(frames,f'BlinkCounter: {blinkcount}',(100,100),colorR=color)
        imgplot=  plotY.update(ratioAvg,color)

        imgstack = cvzone.stackImages([frames,imgplot],2,1)



    cv2.imshow("Image",imgstack)
    cv2.waitKey(1)