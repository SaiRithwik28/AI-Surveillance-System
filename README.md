# 🔒 AI Smart Security & Intrusion Detection System

An intelligent real-time surveillance system built using **YOLOv8**, **OpenCV**, and **Streamlit**. It detects objects from live webcam or uploaded videos, analyzes activity, and generates alerts with severity levels — complete with a live analytics dashboard, detection logs, and event tracking.

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple?style=flat-square)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=flat-square&logo=opencv)

---

## 📸 Demo / Screenshots

<img width="1920" height="983" alt="Screenshot (3)" src="https://github.com/user-attachments/assets/f8edb4df-a4cf-418c-8e67-654996cd9650" />
<img width="1920" height="916" alt="Screenshot (4)" src="https://github.com/user-attachments/assets/e8c303a5-83e0-4d83-9737-b6a90b0ceb86" />
<img width="1920" height="913" alt="Screenshot (5)" src="https://github.com/user-attachments/assets/2b6319da-ecb7-44f7-a0f6-8843cac94fd7" />

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎥 Real-time Detection | Object detection using YOLOv8 on live webcam or uploaded video |
| 🚨 Intrusion Detection | Smart detection with automatic screenshot capture |
| ⚡ Severity Levels | Classifies alerts as Low / Medium / High |
| 📊 Live Dashboard | Real-time analytics with charts and logs |
| 🎛️ Adjustable Settings | Confidence threshold, frame skip, object filters |
| 📁 Export Logs | Download detection logs as CSV or JSON |
| 🖼️ Screenshot Gallery | Auto-captured intrusion images saved as evidence |
| 🧹 Data Reset | Clear all logs and screenshots in one click |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web dashboard and UI |
| YOLOv8 (Ultralytics) | Real-time object detection model |
| OpenCV | Video processing and frame handling |
| Pandas | Detection log management |
| NumPy | Numerical operations |
| Plotly | Interactive charts and analytics |

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/SaiRithwik28/AI-Surveillance-System.git
cd AI_Surveillance_System
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install streamlit opencv-python ultralytics pandas numpy plotly
```

---

## ▶️ Run the Project

```bash
streamlit run Smart.py
```

Then open your browser at `http://localhost:8501` or `http://192.168.31.216:850`

---

## 🧠 How It Works

```
User selects input (Webcam / Video Upload)
        ↓
YOLOv8 processes each frame in real-time
        ↓
Selected objects detected and counted
        ↓
Intrusion logic checks activity patterns
        ↓
Severity level assigned (Low / Medium / High)
        ↓
Alert generated → Screenshot saved as evidence
        ↓
Live dashboard updates with charts and logs
```

---

## 📊 Dashboard Features

1. **Live video feed** — annotated bounding boxes with labels
2. **Intrusion counter** — total intrusions detected
3. **Severity indicator** — real-time threat level
4. **Object statistics** — count per object class
5. **Detection log table** — timestamped history
6. **Alert timeline** — severity-tagged alert feed
7. **Analytics charts** — bar chart, pie chart, confidence over time

---

---

## 🔮 Future Enhancements
📧 Email alert system for intrusion notifications
📱 SMS notifications using Twilio
🧑 Face recognition integration
☁️ Cloud database support (Firebase / AWS)
🌐 Web deployment (Streamlit Cloud / Docker)
🎥 Multi-camera surveillance support

---

## 📋 Requirements

```
streamlit
opencv-python
ultralytics
pandas
numpy
plotly
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 👤 Author

**Maganti Sai Rithwik**
📧 sunnysairithwik@gmail.com
🔗 [GitHub](https://github.com/SaiRithwik28)

---

## ⭐ Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [Streamlit](https://streamlit.io)
- [OpenCV](https://opencv.org)
- [Plotly](https://plotly.com)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE)
