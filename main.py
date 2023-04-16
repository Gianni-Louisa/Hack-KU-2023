"""
Welcome to our face recognition project. This project is based on the face_recognition library.
The project is divided into two parts: One being the front end(Which we didnt finish completely) and the other being the back end which is the facial recognition. Some inspiration came from PySource.
The facial recognition is done by using the face_recognition library. The library is used to detect faces and then encode them. The encoding is then stored in a list. 
Which was then to be processed and sent to the front end for processing. The front end was to be done in HTML and CSS. The front end was to be used to display the number of people in the room,

Project Created by: Gianni Louisa, Jose Leyba, Allie Stratton, and Eli Gabriel
"""
import cv2
from face_recog import Face_Recog
from http import server
import io
import logging
import socketserver
from threading import Condition
from http import server

# Encode faces from a folder
FR = Face_Recog()
FR.processed_images("Face_Detection_Final/images/")
people = 0
# Load Camera
cap = cv2.VideoCapture(0)
same = 2
Jos = True
Gia = True
Eli = True
Allie = True
while True:
    num = 0
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = FR.added_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        if name== "Unknown":
            num += 1
            if num != same:
                people += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
        if name == "Jose Leyba":
            num += 1
            if (Jos):
                people +=1
                Jos = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        if name == "Gianni Louisa":
            if (Gia):
                people +=1
                Gia = False
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 4)
        if name == "Allie Stratton":
            num += 1
            if (Allie):
                people +=1
                Allie = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 200), 4)
        if name == "Eli Gabriel":
            num += 1
            if (Eli):
                people +=1
                Eli = False
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
    
    if num != same:
        print(f"People in screen = {num} ")
        print(f"Total people counted = {people}")
    same = num
        

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

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