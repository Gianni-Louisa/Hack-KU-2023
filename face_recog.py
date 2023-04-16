"""
Welcome to our face recognition project. This project is based on the face_recognition library.
The project is divided into two parts: One being the front end(Which we didnt finish completely) and the other being the back end which is the facial recognition. Some inspiration came from PySource.
The facial recognition is done by using the face_recognition library. The library is used to detect faces and then encode them. The encoding is then stored in a list.
Project Completed by: Gianni Louisa, Jose Leyba, Allie Stratton, and Eli Gabriel.
"""


import face_recognition#pip install face_recognition
import cv2#pip install opencv-python
import os
import glob
import numpy as np

class Face_Recog:#class for the facial recognition
    def __init__(self):#constructor
        self.processed_faces = []#list of known faces
        self.processed_names = []#list of known names

        # Resize frame for a faster speed
        self.frame_resizing = .25#smaller will cause faces to not be seen. Larger will cause the program to run slower(Already very slow)

    def processed_images(self, images_path):#function to load the images
        images_path = glob.glob(os.path.join(images_path, "*.*"))#gets the path of the images, and stores them in a list
        print("{} encoding images found.".format(len(images_path)))#prints the number of images found, if zero adjust path in main.py
        for img_path in images_path:#for loop to go through the images
            img = cv2.imread(img_path)#reads the image
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#converts the image to RGB from BGR, bytes reversed
            file_name = os.path.basename(img_path)#gets the name of the image
            (filename, ext) = os.path.splitext(file_name)#gets file name and splits it from the extension
            # Get encoding
            img_encoding = face_recognition.face_encodings(rgb_img)[0]#gets the encoding of the image

            # Store file name and file encoding
            self.processed_faces.append(img_encoding)#adds the encoding to the list of known faces
            self.processed_names.append(filename)#adds the name to the list of known names
        print("Encoding images loaded")#prints that the images have been loaded, used to know when complete

    def added_faces(self, frame):#function to detect the faces
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)#resizes the frame to the size of the persons head and distance from camera
        # Find all the faces and face encodings in the current frame of video
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)#converts the image to RGB from BGR, bytes reversed
        face_locations = face_recognition.face_locations(rgb_small_frame)#gets the location of the face, for frame
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)#gets the encoding of the face, for frame

        face_names = []#list of names
        for face_encoding in face_encodings:#for loop to go through the face encodings
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(self.processed_faces, face_encoding)#compares the faces
            name = "Unknown"
            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.processed_faces, face_encoding)#gets the distance of the face
            best_match_index = np.argmin(face_distances)#gets the index of the face
            if matches[best_match_index]:#if the face is a match
                name = self.processed_names[best_match_index]#gets the name of the face
            face_names.append(name)#adds the name to the list of names

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)#converts the face locations to a numpy array
        face_locations = face_locations / self.frame_resizing#divides the face locations by the frame resizing
        return face_locations.astype(int), face_names#returns the face locations and names
