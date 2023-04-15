import cv2
from face_recog import SimpleFacerec




# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

# Load Camera
cap = cv2.VideoCapture(0)

while True:
    num = 0
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        if name== "Unknown":
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
        if name == "Jose Leyba":
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)
        if name == "Gianni Louisa":
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 4)
        if name == "Alli Stratton":
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (200, 0, 200), 4)
        if name == "Eli Gabriel":
            num += 1
            cv2.putText(frame, name,(x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 4)
    print(f"People in screen = {num} ")
        

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
