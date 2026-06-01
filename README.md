# 🔒 AI Smart Security & Intrusion Detection System

An intelligent real-time surveillance system built using **YOLOv8, OpenCV, and Streamlit**. It detects objects from live webcam or uploaded videos, analyzes activity, and generates alerts with severity levels. The system also provides a live dashboard with analytics, logs, and event tracking.

---

## 🚀 Features

- 🎥 Real-time object detection using YOLOv8  
- 📷 Supports both **webcam live feed and video upload**  
- 🚶 Detects multiple objects (person, car, motorcycle, etc.)  
- 🚨 Smart intrusion detection system  
- ⚡ Severity classification (Low / Medium / High)  
- 🖼️ Automatic screenshot capture during intrusion events  
- 📊 Live analytics dashboard with charts  
- 📁 Export detection logs (CSV / JSON)  
- 🧹 Clear all data (logs + screenshots)  
- 🎛️ Adjustable confidence threshold  
- ⚡ Frame skipping for faster processing  

---

## 🛠️ Technologies Used

- Python  
- Streamlit  
- OpenCV (cv2)  
- YOLOv8 (Ultralytics)  
- Pandas  
- NumPy  
- Plotly  

---

## 📦 Installation

python -m venv venv
pip install streamlit opencv-python ultralytics pandas numpy plotly

▶️ Run the Project
streamlit run app.py

🧠 How It Works
1.User selects input source (Webcam / Video Upload)
2.YOLOv8 model processes each frame
3.Selected objects are detected and counted
4.Intrusion logic checks activity patterns
5.Severity level is assigned based on rules
6.Alerts are generated and stored
7.Screenshots are saved for evidence
8.Live dashboard updates in real time

📊 Dashboard Features
1.Live video detection feed
2.Intrusion counter
3.Severity indicator
4.Object detection statistics
5.Detection logs table
6.Alert timeline history
7.Charts for analytics

📁 Output Files
/screenshots → Saved intrusion images
Detection logs → CSV / JSON export

🔮 Future Enhancements
1.📧 Email alert system for intrusion
2.📱 SMS notifications using Twilio
3.🧑 Face recognition integration
4.☁️ Cloud database (Firebase / AWS)
5.🌐 Web deployment (Streamlit Cloud / Docker)
6.🎥 Multi-camera surveillance support

⭐ Acknowledgements
1.Ultralytics YOLOv8
2.Streamlit
3.OpenCV
4.Plotly
