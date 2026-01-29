##### **AI Traffic Violation Detection System**



This project is an AI-based traffic monitoring system that detects

vehicles and number plates using computer vision. It extracts the

license plate number using OCR, stores violation data in a database, and

sends automated email alerts.



The goal of this project is to demonstrate how AI can be used in smart

traffic management systems.



###### **What This System Does**



\-   Detects vehicles and number plates using YOLO

\-   Extracts number plate text using OCR

\-   Stores records in MySQL database

\-   Provides backend APIs using FastAPI

\-   Shows results in a Streamlit web app

\-   Sends automatic email notifications for violations



###### **Technologies Used**



* Python
* YOLOv8
* EasyOCR
* FastAPI
* Streamlit
* MySQL
* Gemini API



###### **Project Structure**



AI-Traffic-Violation-Detection-System/



app.py              -> Streamlit frontend

main.py             -> FastAPI backend

yolo\_detect.py      -> YOLO detection logic

ocr.py              -> OCR processing

db.py               -> Database connection

email\_sender.py     -> Email sending logic

gemini\_ai.py        -> Gemini API integration

database(sql).sql  -> MySQL database structure

best.pt             -> Trained YOLO model

requirements.txt    -> Python dependencies

README.md           -> Project documentation





###### **How to Run**



1\.  Install dependencies: pip install -r requirements.txt



2\.  Setup database: Import database(sql).sql into MySQL Update

    credentials in db.py



3\.  Start backend: uvicorn main:app –reload



4\.  Start frontend: streamlit run app.py



###### **Output**



Vehicle detection Plate recognition Database storage Email alerts



###### **Why I Built This**



To practice computer vision, backend development, database integration

and real-world AI systems.



###### **Future Improvements**



* Real-time CCTV video processing
* Improved OCR accuracy
* Cloud deployment
* Mobile app integration
* Detection of more traffic violations



###### **Author Hariom Dixit**



