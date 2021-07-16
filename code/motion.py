import numpy as np
import cv2
import os
# import main as mainfile

# Set global variables and functions
# We need variables for setting the motion level threshold and display font.

# "sdThresh" is used for motion level threshold.
# "font" is used for setting for for text display on video.

sdThresh = 10
font = cv2.FONT_HERSHEY_COMPLEX

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)

    diff32 = frame1_32 - frame2_32  # Difference between two frames

    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)

    dist = np.uint8(norm32*255)

    return dist


cv2.namedWindow('frame')      # GOTO Link for Official Documentation of "namedWindow"
cv2.namedWindow('dist')       # Link: https://docs.opencv.org/2.4/modules/highgui/doc/user_interface.html?highlight=namedwindow

# capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.

cap = cv2.VideoCapture(0)
_, frame1 = cap.read()
_, frame2 = cap.read()

# Begin the main video loop
facecount = 0
while True :
    _, frame3 = cap.read()
    # Get frame3's cols and rows matrix.
    rows, cols, _ = np.shape(frame3)  

    # take the difference between two frames.
    dist = distMap(frame1, frame3)    
    cv2.imshow('dist', frame3)
    dist = distMap(frame1, frame3)
    # Now We can shift our frames.
    frame1 = frame2
    frame2 = frame3

    # Apply Gaussian smoothing to even out our distance mapping.
    mod = cv2.GaussianBlur(dist, (9,9), 0)

    # Threshold this result to retrieve a binary mapping of where motion is taking place.
    _, thresh = cv2.threshold(mod, 100, 255, 0)

    # At this point, we have a binary array that indicates where motion has occurred and where it has not. Now,
    # ..we will use standard deviation to calculate where the motion is significant enough to trigger an alarm.
    _, stDev = cv2.meanStdDev(mod)   # Calculate the standard deviation.


    # Lets show what we found after standard deviation and display that value on the video.
    
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

