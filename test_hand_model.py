import os

model_path = "models/hand_landmarker.task"

if os.path.exists(model_path):
    print("Model found!")
    print("Path:", model_path)
else:
    print("Model NOT found!")