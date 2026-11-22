import os
import time
from datetime import datetime

import cv2
from ultralytics import YOLO

import WhatsAPPSender


CLASS_NAMES = [
    "Grape_Blight_Leaf",
    "Grape_Healthy",
    "Grape_Leaf_Vine_Disease",
    "Grape_Rust_Fungus",
    "Tomato_Leaf_Healthy",
    "Tomato_Leaf_curl_virus",
    "Tomato_Mosaic_virus",
    "Tomato_Yellow_Disease",
]
INFERENCE_FPS = 5
CONFIDENCE_THRESHOLD = 0.70
STABLE_FRAMES_REQUIRED = 20  # 4 seconds at 5 FPS
FRAMES_TO_RESET = 5


def startDetection(farmer_name, mobile_number):
    model = YOLO(os.path.join("model", "best.pt"))
    capture_dir = "Captured_images"
    os.makedirs(capture_dir, exist_ok=True)

    # Most Windows laptops expose the built-in webcam as camera 0.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.release()
        raise RuntimeError(
            "Cannot open camera 0. Check that a webcam is connected and not in use."
        )

    stable_class = None
    stable_count = 0
    missing_count = 0
    notified_this_episode = False
    frame_delay = 1 / INFERENCE_FPS

    try:
        while True:
            loop_started = time.monotonic()
            ret, frame = cap.read()
            if not ret:
                raise RuntimeError("The camera stopped returning frames.")

            result = model.predict(
                source=frame, conf=CONFIDENCE_THRESHOLD, save=False, verbose=False
            )[0]

            confident_boxes = []
            for box in result.boxes:
                class_id = int(box.cls.item())
                confidence = float(box.conf.item())
                if class_id >= len(CLASS_NAMES):
                    continue

                label = CLASS_NAMES[class_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().tolist())
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(
                    frame,
                    f"{label} {confidence:.0%}",
                    (x1, max(y1 - 8, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 0, 255),
                    2,
                )
                confident_boxes.append((confidence, class_id))

            if confident_boxes:
                _, detected_class = max(confident_boxes)
                missing_count = 0
                if detected_class == stable_class:
                    stable_count += 1
                else:
                    stable_class = detected_class
                    stable_count = 1

                if stable_count >= STABLE_FRAMES_REQUIRED and not notified_this_episode:
                    label = CLASS_NAMES[stable_class]
                    description_path = os.path.join("Crop_file", f"{label}.txt")
                    if not os.path.isfile(description_path):
                        raise FileNotFoundError(f"Missing disease description: {description_path}")
                    with open(description_path, "r", encoding="utf-8") as description_file:
                        description = description_file.read()

                    image_name = f"{datetime.now():%Y%m%d_%H%M%S_%f}.jpg"
                    image_path = os.path.join(capture_dir, image_name)
                    if not cv2.imwrite(image_path, frame):
                        raise RuntimeError(f"Could not save detection image: {image_path}")

                    cv2.putText(
                        frame,
                        "Detection confirmed; sending WhatsApp message...",
                        (12, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (0, 180, 0),
                        2,
                    )
                    cv2.imshow("Crop Disease Detection System", frame)
                    cv2.waitKey(1)
                    WhatsAPPSender.sendInfoWA(
                        mobile_number, image_path, label, description, farmer_name
                    )
                    print(f"Detection sent to WhatsApp; image saved at {image_path}")
                    notified_this_episode = True
            else:
                missing_count += 1
                if missing_count >= FRAMES_TO_RESET:
                    stable_class = None
                    stable_count = 0
                    notified_this_episode = False

            cv2.imshow("Crop Disease Detection System", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            time.sleep(max(0, frame_delay - (time.monotonic() - loop_started)))
    finally:
        cap.release()
        cv2.destroyAllWindows()
