import cv2
import mediapipe as mp
import time

# ==============================
# 1. MediaPipe model
# ==============================

MODEL_PATH = "models/hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


# ==============================
# 2. Hand Landmarker settings
# ==============================

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1
)

landmarker = HandLandmarker.create_from_options(options)


# ==============================
# 3. Camera
# ==============================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened!")
    exit()

print("Hand tracking started!")
print("Move your hand UP to FLAP!")
print("Press Q to quit.")


# ==============================
# 4. Variables
# ==============================

previous_y = None

FLAP_THRESHOLD = 15
FLAP_COOLDOWN = 0.4

last_flap_time = 0


# ==============================
# 5. Main loop
# ==============================

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read frame!")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    # BGR → RGB
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
    result = landmarker.detect(mp_image)

    flap = False


    # ==============================
    # 6. Hand detected
    # ==============================

    if result.hand_landmarks:

        hand = result.hand_landmarks[0]

        # Wrist = landmark 0
        wrist = hand[0]

        current_y = int(
            wrist.y * frame.shape[0]
        )


        # ==============================
        # 7. Calculate movement
        # ==============================

        if previous_y is not None:

            movement = previous_y - current_y

            current_time = time.time()

            if (
                movement > FLAP_THRESHOLD
                and current_time - last_flap_time > FLAP_COOLDOWN
            ):

                flap = True
                last_flap_time = current_time

        previous_y = current_y


        # ==============================
        # 8. Display Y position
        # ==============================

        cv2.putText(
            frame,
            f"Hand Y: {current_y}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )


        # ==============================
        # 9. Display FLAP
        # ==============================

        if flap:

            cv2.putText(
                frame,
                "FLAP!",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 255, 0),
                3
            )


        # ==============================
        # 10. Draw landmarks
        # ==============================

        for landmark in hand:

            x = int(
                landmark.x * frame.shape[1]
            )

            y = int(
                landmark.y * frame.shape[0]
            )

            cv2.circle(
                frame,
                (x, y),
                5,
                (0, 255, 0),
                -1
            )


    # ==============================
    # 11. Show camera
    # ==============================

    cv2.imshow(
        "Flappy Bird Hand Control",
        frame
    )


    # Q → quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==============================
# 12. Cleanup
# ==============================

cap.release()
cv2.destroyAllWindows()
landmarker.close()

print("Program finished.")