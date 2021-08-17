# Import the required libraries
import cv2
import imutils
import imageio
import time
import numpy as np

# Create a video capture instance.
# VideoCapture(0) corresponds to your computers
# webcam
cap = cv2.VideoCapture(0)

# Lets grab the frames-per-second (FPS) of the
# webcam so our output has a similar FPS.
# Lets also grab the height and width so our
# output is the same size as the webcam
fps          = cap.get(cv2.CAP_PROP_FPS)
frame_width  = int(cap.get(3))
frame_height = int(cap.get(4))

# Now lets create the video writer. We will
# write our processed frames to this object
# to create the processed video.
out = cv2.VideoWriter('outpy.avi', 
    cv2.VideoWriter_fourcc('M','J','P','G'), 
    fps, 
    (frame_width,frame_height)
)

frames = []

cv2.namedWindow('Video')

blackLower = (0, 0, 0)
blackUpper = (50, 50, 50)

time.sleep(2)

def blur_and_mask(frame, lower_color, upper_color):
    blurred = cv2.GaussianBlur(frame, (5, 5), 3)
    mask = cv2.inRange(blurred, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    return mask

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Grayscale the image and apply a gaussian blur to it
    
    mask = blur_and_mask(frame, blackLower, blackUpper)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cnts = cv2.findContours(
        mask.copy(), 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )

    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        c    = max(cnts, key=cv2.contourArea)
        rect = cv2.boundingRect(c)

        # This area is too small to be of our
        # interest, disregard it and go to the
        # next frame
        if rect[2] < 100 or rect[3] < 100: continue

        # Unpack the bounding box
        x,y,w,h = rect
        y1 = y
        y2 = y + h
        x1 = x
        x2 = x + w
        # Draw the bounding box on the frame
        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (0,255,0),
            2
        )

        # Take a canny edge detection of the newly drawn
        # rectangle from the original grey scale image.
        # This will perform edge detection in only the 
        # area of interect (the cv2 rectangle defined above).
        # This will make all the edges white and the
        # rest of the pixels black. So, we have to invert it
        # so the black becomes white and the 
        # white becomes black (to fit the AHA video)
        to_canny = cv2.GaussianBlur(
            gray[y:y+h, x:x+w],
            (5, 5),
            3
        )

        edges = cv2.bitwise_not(
            cv2.Canny(to_canny, 0, 50)
        )

        # Since the edges are only a 2-channel frame,
        # we can overlay it on to each channel in the 
        # original frame
        frame[y1:y2, x1:x2, 0] = edges
        frame[y1:y2, x1:x2, 1] = edges
        frame[y1:y2, x1:x2, 2] = edges

    out.write(frame)
    frames.append(frame)
    # Display the resulting frame
    cv2.imshow('Video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()

fp_out = "../../../static/assets/img/take-on-me.gif"
with imageio.get_writer(fp_out, mode="I") as writer:
  for idx, frame in enumerate(frames[0:60]):
        print("Adding frame to GIF file: ", idx + 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        writer.append_data(rgb_frame)