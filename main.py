from imutils.video import FPS
import imutils
import cv2


video = input('Enter video path or camera number: ')
tracker = cv2.TrackerCSRT_create()
initBB = None


try:
	video = int(video)
except:
	pass

cap = cv2.VideoCapture(video)


# initialize the FPS throughput estimator
fps = None

# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	success, frame = cap.read()
	# check to see if we have reached the end of the stream
	if not success:
		break
	# resize the frame (so we can process it faster) and grab the
	frame = imutils.resize(frame, height=1000)
	(H, W) = frame.shape[:2]
	# frame dimensions
	# frame = imutils.resize(frame, width=500)
		# check to see if we are currently tracking an object
	if initBB is not None:
		print('runn')
		# grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)
		# check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h),
				(0, 255, 0), 2)
		# update the FPS counter
		fps.update()
		fps.stop()
		# initialize the set of information we'll be displaying on
		# the frame
		info = [
			("FPS", "{:.2f}".format(fps.fps())),
		]
		# loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
				cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
			
	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		initBB = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		
		x1, y1, w, h = initBB
		x2 = x1+w
		y2 = y1+h
		cv2.rectangle(frame,(x1,y1), (x2,y2), (0,255,0),5)
		
		cv2.imwrite('sample.jpg',frame)

		print(initBB, 'COORDS')
		# start OpenCV object tracker using the supplied bounding box
		# coordinates, then start the FPS throughput estimator as well
		tracker.init(frame, initBB)
		fps = FPS().start()
	# if the `q` key was pressed, break from the loop
	elif key == ord("q"):
		break

cv2.destroyAllWindows()

