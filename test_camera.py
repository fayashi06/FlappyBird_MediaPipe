import cv2
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened!")
    exit()

print("Camera is working!")
print("Press Q to close.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Could not read camera frame!")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release() #camerani release edir(serbest buraxir)
cv2.destroyAllWindows() #butun cv2 pencerelerini close edir