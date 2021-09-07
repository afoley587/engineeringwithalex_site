import face_recognition
import os
import glob
import cv2 
import numpy as np
import time 
from userauth import do_login

        
is_awake = False

def awake_callback():
    input("click enter to start...")
    return

class FacialData:
    def __init__(self):
        self.names     = []
        self.encodings = []
        self.images    = []
    
    def train(self, file_list, names):
        if (len(file_list) != len(names)):
            print("ERR! The file list and name list are not equal")
            return

        for i in range(len(file_list)):
            img      = face_recognition.load_image_file(list_of_files[i])
            encoding = face_recognition.face_encodings(img)[0]
            self.images.append(img)
            self.encodings.append(encoding)
            self.names.append(names[i])

def gather_files(extension_glob='*.jpg', location=None) -> (list, list):
    if (not location):
        script_dir = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
        location = os.path.join(script_dir, 'data', 'faces')

    list_of_files = [f for f in glob.glob(os.path.join(location, extension_glob))]
    list_of_names = [f.split(os.path.sep)[-1].split('.')[0] for f in list_of_files]
    return (list_of_files, list_of_names)

list_of_files, names = gather_files()
number_files = len(list_of_files)
fd = FacialData()
fd.train(list_of_files, names)
print(list_of_files, names)

face_locations = []
face_encodings = []
face_names = []
video_capture = cv2.VideoCapture(0)
sampling_frame_number  = 0
sampling_rate          = 3
awake_frame_number     = 0
awake_timeout          = 100 # should make this (frames / sec) * ( desired mins ) * ( sec / min )

while True:
    sampling_frame_number = (sampling_frame_number + 1) % sampling_rate  
    awake_frame_number    = (awake_frame_number + 1) % awake_timeout  
    if (awake_frame_number == 0): awake_callback()
    if (sampling_frame_number != 0): continue
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]
    name = ""

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    face_names = []
    for index, face_encoding in enumerate(face_encodings):
        matches = face_recognition.compare_faces(fd.encodings, face_encoding)
        face_distances = face_recognition.face_distance(fd.encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = fd.names[best_match_index]
            face_names.append(name)
        else:
            face_locations.pop(index)

    found_faces = (len(face_names) > 0) and (len(face_locations) > 0)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if (name) == "" : continue
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Input text label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    if (found_faces):
        do_login(face_names[0])
        time.sleep(5)

    