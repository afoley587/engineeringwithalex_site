# Re-creating (simply) the Take On Me Music Video

## Overview :material-deathly-hallows:
So, what's the endgoal here? Well, if you're anything like me, you may
like 80's music. Even better, you may like 80's music videos. Well
the "Take On Me" music video is one of my absolute favorites. The
smooth morphing from full color to black/white was always super cool
to me. As soon as I started working with OpenCV, Edge detectors, etc.
I saw a small opportunity to put myself in to the music video, and that's
what we are going to do today :fontawesome-regular-laugh-wink:.

Now, this is going to be a pretty simple rendition to the great music video.
We will just be using OpenCV to...:

* color mask video frames to track a single object
* find the edges in the above mask
* overlay the mask on the original frame

In the end, you will have a gif and a video representation to show your friends.

## Getting Started :fontawesome-solid-wrench:
If you're using poetry (like me), the most relevant entries in your toml will
be: 
```shell
imutils = "0.5.4"
opencv-python = "4.5.3.56"
imageio = "2.9.0"
```

If you're not (and you're using `pip`), you can pip install the below:
```shell
pip install opencv-python==4.5.3.56 imageio==2.9.0 imutils==0.5.4
```

Now, you're all set up.

## The Code :octicons-code-square-16:
So, lets run through the code...

### The Setup
So, for the setup.

The first thing we have to do is import our required libraries. 

```python
# Import the required libraries
import cv2
import imutils
import imageio
import time
```

Next, we can set up our video streaming from our local webcam.
Its also important that we set our output stream to have the same
FPS, frame width, and frame height as our input stream.
```python
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
```

Moving forward, we can initialize our outputs.
The `out` object is a video writer. What that means
is that as we write frames to it, it will save these
frames to the file we designate. If we look at the
object instantiation below, we are going to write
the video stream to `output.avi` with `MJPG` encoding.
And if you notice, it will have the same FPS and size as
our webcam.

The `frames` list will be used to create our gif in the end.

Finally, we create a named window so we can see what our code 
is doing realtime!

```python
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
```

As I previously noted, we are going to use simple
color masking to create our video. In the below, 
we will use the lower end of that mask as pure black
(0, 0, 0) and the upper end will be a dark grey (50, 50, 50).
```python
blackLower = (0, 0, 0)
blackUpper = (50, 50, 50)
```

### Helper Functions
This helper function is going to do some super fun stuff.
  
First, it will blur the frame we give it. It's usually 
important to blur your frames before applying filters to
them. The decreased resolution will bring forth the more 
prominent features of the frame and reduce noise.
  
Second, we will apply the color mask to the frame.

Third, we will erode the mask. Erosion is another technique
to reduce noise by calculating a local minimum over
some kernel (in our case, a 5x5 kernel).
```python
def blur_and_mask(frame, lower_color, upper_color):
    blurred = cv2.GaussianBlur(frame, (5, 5), 3)
    mask = cv2.inRange(blurred, blackLower, blackUpper)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    return mask
```

### Main Loop

Now that all of the setup is out of the way, we
can start playing with the main loop!

The first portion of this loop might look easy to you.
We:

* Read a frame from our webcam (video stream defined above)
* We use our fancy function above to retrieve a color mask of the frame
* We then create a greyscale copy of the original frame (we will use this later!)

```python
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Grayscale the image and apply a gaussian blur to it
    
    mask = blur_and_mask(frame, blackLower, blackUpper)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
```

But, now its starting to get interesting!
We use `cv2.findContours` to grab all of our contours from
our image mask. The `cv2.RETR_EXTERNAL` tells us to only
retrieve the extreme outer contours. The `cv2.CHAIN_APPROX_SIMPLE`
tells openCV to compress all of the directional line segments
(horizontal, vertical, diagonal) and leave only their end points.

Finally, we use `imutils.grab_contours` which just helps
us differentiate which version of OpenCV is running 
and use the contours appropriately.

```python
    cnts = cv2.findContours(
        mask.copy(), 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )

    cnts = imutils.grab_contours(cnts)
```

Next is probably the most complex piece of code,
but its not too bad once we break it down!

First, we retrieve the biggest contour from our frame.
This will be object that had the most points matching
the specified color range. We can then build a bounding
rectangle around that contour.
```python
    if len(cnts) > 0:
        c    = max(cnts, key=cv2.contourArea)
        rect = cv2.boundingRect(c)

        # This area is too small to be of our
        # interest, disregard it and go to the
        # next frame
        if rect[2] < 100 or rect[3] < 100: continue
```

The problem with the above is that `cv2.boundingRect(c)`
doesn't actually draw anything on the frame for us. So,
if we want to draw it on there (and we DO), we will have
to do that ourselves. What `cv2.boundingRect(c)` does give us
is a tuple of starting x-coordinate, starting y-coordinate, 
rectangle width, and rectangle height.
  
Coincidentally, this is exactly what we need to draw a box
on the frame!
```python
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
```

Up to this point, we have a frame with a box drawn on it. That's
close, but not exactly what we were going for! Remember, we want
the inside of that box to look like the "Take On Me" music video
(where the color is subtracted).

To do that, we will need two things:

* The greyscale frame from above
* The bounding rectangle from above

The `gray[y:y+h, x:x+w]` will take the pixels from the
greyscale image that fall within the bounding box. Always
remember, images and frames are just matrices!
  
Once we have that area of interest, we can apply the Canny
edge detection filter to it. This filter will give us a frame
that is all black except for the detected edges, they will be 
white. The next action is to do a `bitwise_not` of the edge
detected frame. That way, everything will be white except for
the edges (they will be black).
  
Finally, we can overlay that new frame-segment on to our 
original frame, write it to our output stream, and bam...
were done!
```python
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

```

### Making a gif
So at this point, we have our music video and its
written to disk. I also wanted to create a little gif
of this to use as a thumbnail. Below is some code
using `imageio` to do just that.
```python
fp_out = "../../../static/assets/img/take-on-me.gif"
with imageio.get_writer(fp_out, mode="I") as writer:
  for idx, frame in enumerate(frames[0:60]):
        print("Adding frame to GIF file: ", idx + 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        writer.append_data(rgb_frame)
```

## Running :fontawesome-solid-running:
Running can simply be done with `python main.py`!