"""
Welcome to our face recognition project. This project is based on the face_recognition library.
The project is divided into two parts: One being the front end(Which we didnt finish completely) and the other being the back end which is the facial recognition. Some inspiration came from PySource.
The facial recognition is done by using the face_recognition library. The library is used to detect faces and then encode them. The encoding is then stored in a list. 
Which was then to be processed and sent to the front end for processing. The front end was to be done in HTML and CSS. The front end was to be used to display the number of people in the room,

Project Created by: Gianni Louisa, Jose Leyba, Allie Stratton, and Eli Gabriel
"""
import cv2# Importing OpenCV-Python
from face_recog import Face_Recog# Importing the face recognition class
from http import server# Importing the server
import io# Importing the input output library
import logging# Importing the logging library
import socketserver# Importing the socket server library
from threading import Condition# Importing the threading library
from http import server# Importing the server library

# Encode faces from a folder
FR = Face_Recog()# Creating an instance of the Face_Recog class
FR.processed_images("Face_Detection_Final/images/")# Processing the images in the images folder
people = 0# Variable to keep track of the number of people in the room
cap = cv2.VideoCapture(0)# Creating a video capture object
same = 2# Variable to make sure it isnt double counted
Jos = True#member names intitialized to true
Gia = True#member names intitialized to true
Eli = True#member names intitialized to true
Allie = True#member names intitialized to true
while True:# Loop to keep the program running
    num = 0#num var
    ret, frame = cap.read()# Reading the frame

    # Detect Faces
    face_locations, face_names = FR.added_faces(frame)# Detecting the faces in the frame
    for face_loc, name in zip(face_locations, face_names):# Loop to draw the rectangles around the faces
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]# Getting the coordinates of the rectangle
        if name== "Unknown":# If the name is unknown then it will be red
            num += 1# Adding one to the number of people in the room
            if num != same:# If the number of people in the room is not the same as the previous frame then it will print the number of people in the room
                people += 1# Adding one to the total number of people in the room
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)# Drawing the text on the frame will be red B,G,R
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)# Drawing the rectangle around the face will be red B,G,R
        if name == "Jose Leyba":# If the name is Jose then it will be green
            num += 1
            if (Jos):
                people +=1
                Jos = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        if name == "Gianni Louisa":# If the name is Gianni then it will be light blue
            if (Gia):
                people +=1
                Gia = False
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 4)
        if name == "Allie Stratton":# If the name is Allie then it will be purple
            num += 1
            if (Allie):
                people +=1
                Allie = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 200), 4)#
        if name == "Eli Gabriel":# If the name is Eli then it will be blue
            num += 1
            if (Eli):
                people +=1
                Eli = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
    
    if num != same:# If the number of people in the room is not the same as the previous frame then it will print the number of people in the room
        print(f"People in screen = {num} ")# Printing the number of people in the room
        print(f"Total people counted = {people}")# Printing the total number of people in the room
    same = num# Setting the same variable to the number of people in the room
        

    cv2.imshow("Frame", frame)# Displaying the frame

    key = cv2.waitKey(1)# Waiting for a key to be pressed
    if key == 27:# If the key is the escape key then it will break the loop
        break# Breaking the loop

#This was our attempt at an HTTP Server to hopefully stream out frame to a webpage to use as a front end but wasnt able to do it in time.
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


cap.release()
cv2.destroyAllWindows()