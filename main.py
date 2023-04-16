"""
Welcome to our face recognition project. This project is based on the face_recognition library.
The project is divided into two parts: One being the front end(Which we didnt finish completely) and the other being the back end which is the facial recognition. Some inspiration came from PySource.
The facial recognition is done by using the face_recognition library. The library is used to detect faces and then encode them. The encoding is then stored in a list. 
Which was then to be processed and sent to the front end for processing. The front end was to be done in HTML and CSS. The front end was to be used to display the number of people in the room,

Project Completed by: Gianni Louisa, Jose Leyba, Allie Stratton, and Eli Gabriel
"""

import cv2#pip install opencv-python
from face_recog import Face_Recog#pip install face_recognition
from http import server#pip install http
import io#pip install io
import logging#pip install logging
import socketserver#pip install socketserver
from threading import Condition#pip install threading

# Encode faces from a folder
sfr = Face_Recog()
sfr.load_encoding_images("Face_Detection_Final/images/")#images folder if taking straight from github images/ is all youll need, source of many errors
people = 0#number of people in the room
# Load Camera
cap = cv2.VideoCapture(0)#0 is the default camera, 1 is the second camera, etc
same = 2#number of times the same person can be detected
Jos = True#boolean for if the person is in the room
Gia = True#boolean for if the person is in the room
Eli = True#boolean for if the person is in the room
Allie = True#boolean for if the person is in the room
while True:#main loop
    num = 0#number of people detected
    ret, frame = cap.read()#read the camera

    # Detect Faces, and if one of known 4 team members is detected special colors assigned to borders. Else green for known, red for unknown
    face_locations, face_names = sfr.detect_known_faces(frame)#detecting locations and names of known faces
    for face_loc, name in zip(face_locations, face_names):#looping through the locations and names
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]#getting the coordinates of the face
        if name== "Unknown":#if the name is unknown
            num += 1#add one to the number of people detected
            if num != same:#if the number of people detected is not the same as the last time
                people += 1#add one to the number of people in the room
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)#putting the name on the screen
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)#putting a rectangle around the face with a red border (R,G,B)
        if name == "Jose Leyba":#if the name is Jose
            num += 1
            if (Jos):
                people +=1
                Jos = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        if name == "Gianni Louisa":#if the name is Gianni
            if (Gia):
                people +=1
                Gia = False
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 4)
        if name == "Allie Stratton":#if the name is Allie
            num += 1
            if (Allie):
                people +=1
                Allie = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 200), 4)
        if name == "Eli Gabriel":#if the name is Eli
            num += 1
            if (Eli):
                people +=1
                Eli = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
    
    if num != same:#if the number of people detected is not the same as the last time
        print(f"People in screen = {num} ")#print the number of people detected
        print(f"Total people counted = {people}")#print the number of different people that have been detected in front of the camera since starting.
    same = num#set the same variable to the number of people detected
        

    cv2.imshow("Frame", frame)#show the frame with the faces detected

    key = cv2.waitKey(1)#wait for a key to be pressed
    if key == 27:#if the key is the escape key
        break
    
    cap.release()#release the camera
    cv2.destroyAllWindows()#close all windows



#Attempt to make a HTTP server to stream the video to a webpage, since we wanted a front end to add to known users and to display the number of people in the room.
#However were getting bugs due to cv2 and the http server not playing nice together, so we decided to just use the terminal to display the number of people in the room.
#This code is not used in the final product, but we wanted to keep it in the code for future reference.
"""
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/front-end.html')
            self.end_headers()
        elif self.path == '/front-end.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with frame as camera:
    actuator.init(50)
    output = StreamingOutput()
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
"""
