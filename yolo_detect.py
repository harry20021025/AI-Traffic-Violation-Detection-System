import cv2
from ultralytics import YOLO
import os

model = YOLO("best.pt")

def detect_plate(image_path):

    img = cv2.imread(image_path)

    if img is None:
        print("ERROR: Image not read:", image_path)
        return None

    results = model(img, conf=0.10, iou=0.3)

    if len(results) == 0 or results[0].boxes is None:
        print("YOLO ran but no boxes object")
        return None

    boxes = results[0].boxes

    if len(boxes) == 0:
        print("YOLO found 0 boxes")
        return None

    best_box = None
    best_area = 0

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        area = (x2 - x1) * (y2 - y1)
        if area > best_area:
            best_area = area
            best_box = (x1, y1, x2, y2)

    if best_box is None:
        print("No valid box selected")
        return None

    x1, y1, x2, y2 = best_box
    plate = img[y1:y2, x1:x2]

    if plate.size == 0:
        print("Cropped plate is empty")
        return None

    os.makedirs("uploads", exist_ok=True)

    plate_path = "uploads/plate.jpg"
    cv2.imwrite(plate_path, plate)

    print("Plate detected and saved:", plate_path)
    return plate_path
