from fastapi import FastAPI, UploadFile, File, HTTPException, Form, BackgroundTasks
import shutil
import os

from yolo_detect import detect_plate
from ocr import extract_number
from db import get_owner, save_fine, get_violation_fine
from email_sender import send_email

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/process-image")
async def process_image(
    file: UploadFile = File(...),
    violation_type: str = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    try:
        # 1️⃣ Save image
        image_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2️⃣ Detect plate
        plate_path = detect_plate(image_path)
        if not plate_path:
            return {"error": "Number plate not detected"}

        # 3️⃣ OCR
        vehicle_no = extract_number(plate_path, debug=True)
        if not vehicle_no:
            return {"error": "OCR failed"}

        # 4️⃣ DB lookup (ONCE)
        owner = get_owner(vehicle_no)
        if not owner or len(owner) < 2:
            return {"error": "Invalid owner data in database"}

        owner_name = owner[0]
        email = owner[1]

        # 5️⃣ Get fine
        fine = get_violation_fine(violation_type)

        # 6️⃣ Send email in background
        background_tasks.add_task(
            send_email,
            email,
            owner_name,
            vehicle_no,
            fine,
            violation_type
        )

        # 7️⃣ Save fine
        save_fine(vehicle_no, email, fine, violation_type)

        return {
            "vehicle_number": vehicle_no,
            "owner_name": owner_name,
            "email": email,
            "violation_type": violation_type,
            "fine": fine,
            "status": "Fine generated & email sent"
        }

    except Exception as e:
        print("BACKEND ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
