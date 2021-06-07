import numpy as np
import cv2
import os


sdThresh = 10
font = cv2.FONT_HERSHEY_COMPLEX

def distMap(frame1, frame2):
  
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)

    diff32 = frame1_32 - frame2_32  # Difference between two frames

    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)

    dist = np.uint8(norm32*255)

    return dist


cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
_, frame2 = cap.read()


while True :
    _, frame3 = cap.read()
  
    rows, cols, _ = np.shape(frame3)  

    # take the difference between two frames.
    dist = distMap(frame1, frame3)    

    frame1 = frame2
    frame2 = frame3

    
    cv2.imshow('dist', mod)
    cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)

    # If standard deviation is more than our threshold, then print a message.
    if stDev > sdThresh:
        print("Motion detected.. Do something!!!")
        cap.release()
        cv2.destroyAllWindows()
        import main as mainfile
        mainfile       


    
    cv2.imshow('frame', frame2)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()