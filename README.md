###### **AI Traffic Violation Detection System**

This project is an AI-based traffic monitoring system that detects vehicles and number plates using computer vision.
It extracts the license plate number using OCR, stores violation data in a database, and sends automated email alerts.

The goal of this project is to demonstrate how AI can be used in smart traffic management systems.

###### **What This System Does**

Detects vehicles and number plates using YOLO

Extracts number plate text using OCR

Stores records in MySQL database

Provides backend APIs using FastAPI

Shows results in a Streamlit web app

Sends automatic email notifications for violations

🛠 Technologies Used

Python

YOLOv8

EasyOCR

FastAPI

Streamlit

MySQL

Gemini API

📁 Project Structure
AI-Traffic-Violation-Detection-System/

app.py               -> Streamlit frontend
main.py              -> FastAPI backend
yolo_detect.py       -> YOLO detection logic
ocr.py               -> OCR processing
db.py                -> Database connection
email_sender.py      -> Email sending logic
gemini_ai.py         -> Gemini API integration
database(sql).sql   -> MySQL database structure
best.pt              -> Trained YOLO model
requirements.txt     -> Python dependencies
README.md            -> Project documentation

📊 Dataset & Model Training

This project uses an Indian Number Plate Dataset for training the YOLO model.

📁 Dataset Source

Roboflow Universe dataset:

🔗 https://universe.roboflow.com/yolox-qcftu/indian-number-plate-keeo5/dataset/2

📈 Dataset Split

Training set: 1215 images

Validation set: 78 images

Testing set: 59 images

🤖 Model Training

The YOLO model was trained on the above dataset

Best trained model saved as:

best.pt


This model is used for number plate detection in the system.

⚙️ How to Run the Project
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Setup database

Import database(sql).sql into MySQL

Update database credentials in db.py

3️⃣ Start backend
uvicorn main:app --reload

4️⃣ Start frontend
streamlit run app.py

📊 Output

Vehicle detection

Plate recognition

Violation record storage

Automated email alerts

🎯 Why I Built This

This project was built to practice:

Computer vision

Backend API development

Database integration

Real-world AI systems

🚀 Future Improvements

Real-time CCTV video processing

Improved OCR accuracy

Cloud deployment

Mobile app integration

Detection of more traffic violations

👨‍💻 Author

Hariom Dixit



