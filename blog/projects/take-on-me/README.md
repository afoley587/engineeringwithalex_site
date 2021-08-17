# Re-creating (simply) the Take On Me Music Video

## Overview
So, what's the endgoal here? Well, if you're anything like me, you may
like 80's music. Even better, you may like 80's music videos. Well
the "Take On Me" music video is one of my absolute favorites. The
smooth morphing from full color to black/white was always super cool
to me. As soon as I started working with OpenCV, Edge detectors, etc.
I saw a small opportunity to put myself in to the music video, and that's
what we are going to do today :smile:.

Now, this is going to be a pretty simple rendition to the great music video.
We will just be using OpenCV to...:
* color mask video frames to track a single object
* find the edges in the above mask
* overlay the mask on the original frame

In the end, you will have a gif and a video representation to show your friends.

## Getting Started
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

## The Code
So, lets run through the code...

### The Setup
So, for the setup.

## Running

## Viewing