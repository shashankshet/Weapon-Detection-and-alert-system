import cv2
import numpy as np
import time 
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from datetime import datetime


#Load YOLO
net = cv2.dnn.readNet("C:/Users/Shashank/Desktop/gun/yolov3_custom_train_final.weights","C:/Users/Shashank/Desktop/gun/yolov3_custom_train.cfg")
classes = []
with open("yolo.names","r") as f:
	classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i[0]-1] for i in net.getUnconnectedOutLayers()]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]



# Loading images
cap = cv2.VideoCapture(0)
time_start = time.time()
frame_id = 0
font = cv2.FONT_HERSHEY_COMPLEX



def name():
	# This function is used to give a unique name to saved output file based on time
	now = datetime.now()

	current_time = now.strftime("%H:%M:%S")
	return current_time
	#return ''.join(map(str, current_time))











# Make call function 
def make_call():
	# Your Account Sid and Auth Token from twilio.com/console
	# DANGER! This is insecure. See http://twil.io/secure
	account_sid = #insert twilio sid here
	auth_token = #insert auth token here
	client = Client(account_sid, auth_token)

	call = client.calls.create(
	                        url ='http://demo.twilio.com/docs/voice.xml',
	                        to = #registered_phno
	                        from_=#received phno
	                    )

	print("Weapon detected!! Sending call alert")



# fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# out = cv2.VideoWriter('C:/Users/Shashank/Desktop/gun/output.avi', fourcc, 20.0, (640,480))


# fourcc = cv2.VideoWriter_fourcc(*'mpv4')
# out = cv2.VideoWriter(name(),fourcc, 20.0, (640,480), True)
# out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480), True)



while True:
	_,frame = cap.read()
	frame_id+= 1

	#  Save Video: FourCC is a 4-byte code used to specify the video codec.
	#  The list of available codes can be found in fourcc.org. It is platform dependent.

	# * In Fedora: DIVX, XVID, MJPG, X264, WMV1, WMV2. (XVID is more preferable. MJPG results in high size video. X264 gives very small size video)
	# * In Windows: DIVX (More to be tested and added)
	#  FourCC code is passed as cv2.VideoWriter_fourcc('M','J','P','G') OR
	#  cv2.VideoWriter_fourcc(*'MJPG') for MJPG.
	fourcc = cv2.VideoWriter_fourcc(*'XVID')
	out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480), True)
	out.write(frame)
	# print("saving!!")




	height, width, channels = frame.shape


	# Detecting Objects
	blob = cv2.dnn.blobFromImage(frame, 0.00392, (320,320), (0,0,0), True,crop=False)



	# Feeding to nets
	net.setInput(blob)
	outs = net.forward(output_layers)


	# Showing informations on the screen 
	class_ids = []
	confidences = []
	boxes = []


	# Showing informations on screen 
	for out in outs:
		for detection in out:
			scores = detection[5:]
			class_id = np.argmax(scores)
			confidence = scores[class_id]
			if confidence > 0.5:
				# Object Detected
				center_x = int(detection[0] * width)
				center_y = int(detection[1] * height)
				w = int(detection[2] * width)
				h = int(detection[3] * height)
				
				# Rectangle Co-Ordinate
				x = int(center_x - w/2)
				y = int(center_y - h/2)


				boxes.append([x, y, w, h])
				confidences.append(float(confidence))
				class_ids.append(class_id)
			if confidence > 0.9:
				# Make call Function
				make_call()
				
				

	indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
	print(indexes)
	font = cv2.FONT_HERSHEY_COMPLEX

	for i in range(len(boxes)):
		if i in range(len(boxes)):
				x, y, w, h =boxes[i]
				label = str(classes[class_ids[i]])
				color = colors[i]
				label = label+"; confidence:  "+repr(confidences[i])
				cv2.rectangle(frame, (x,y), (x + w, y + h), color, 2)
				cv2.putText(frame, label, (x, y+30),font, 0.5, color, 2)



	elapsed_time = time.time() - time_start
	fps = frame_id / elapsed_time
	cv2.putText(frame, "FPS:  "+str(fps), (10,30), font, 0.5, (0,0,0), 1)
	cv2.imshow("Video",frame) 

	key = cv2.waitKey(1)
	if key == 27:
		break;

cap.release()  # Commenting this line will keep the camera alive all the time
out.release()  # release "out" variable of videowriter
cv2.destroyAllWindows()
