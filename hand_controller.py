import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ==================================================
# MODEL
# ==================================================

MODEL_PATH = "models/hand_landmarker.task"


# ==================================================
# MEDIAPIPE
# ==================================================

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1
)

detector = vision.HandLandmarker.create_from_options(
    options
)


# ==================================================
# CAMERA
# ==================================================

camera = cv2.VideoCapture(0)


# ==================================================
# MAIN LOOP
# ==================================================

while True:

    success, frame = camera.read()

    if not success:
        print("Camera error!")
        break


    # Mirror image

    frame = cv2.flip(
        frame,
        1
    )


    # OpenCV BGR → RGB

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # MediaPipe image

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )


    # Detect hand

    result = detector.detect(
        mp_image
    )


    # ==================================================
    # HAND DETECTED
    # ==================================================

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        # Index finger tip

        index_finger = hand[8]

        x = index_finger.x
        y = index_finger.y


        # Convert coordinates

        pixel_x = int(
            x * frame.shape[1]
        )

        pixel_y = int(
            y * frame.shape[0]
        )


        # Draw index finger point

        cv2.circle(
            frame,
            (
                pixel_x,
                pixel_y
            ),
            10,
            (0, 255, 0),
            -1
        )


        # Display Y value

        cv2.putText(
            frame,
            f"Y: {y:.2f}",
            (
                20,
                40
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )


    # ==================================================
    # SHOW CAMERA
    # ==================================================

    cv2.imshow(
        "Ginger Hand Controller",
        frame
    )


    # ESC → EXIT

    if cv2.waitKey(1) & 0xFF == 27:
        break


# ==================================================
# EXIT
# ==================================================

camera.release()

cv2.destroyAllWindows()