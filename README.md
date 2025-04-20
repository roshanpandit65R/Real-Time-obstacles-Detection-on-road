# 🚗 Real-Time Road Object Detection with Distance Estimation and Voice Alert

This project uses **YOLOv8**, **OpenCV**, and **Flask** to detect relevant road objects in real-time using a webcam. If any object is detected within a close range (e.g., < 500 cm), the system alerts the user with both a **visual warning** on the screen and a **voice message** saying _"Slow down your car!"_.

---

### 📸 Features

- ✅ Real-time object detection using YOLOv8
- ✅ Estimates distance of detected objects using bounding box dimensions
- ✅ Displays bounding boxes and class names with estimated distance
- ✅ Alerts with on-screen message: `"SLOW DOWN YOUR CAR!"`
- ✅ **Voice alert** using text-to-speech when an object is too close
- ✅ Web interface using Flask with live video feed

---

### 🛠 Tech Stack

| Tool         | Description                          |
|--------------|--------------------------------------|
| Python       | Programming Language                 |
| YOLOv8       | Object Detection Model (Ultralytics) |
| OpenCV       | Real-time video processing           |
| Flask        | Web server to serve live feed        |
| pyttsx3      | Text-to-speech engine for alerts     |

---

### 📂 Folder Structure

```
.
├── app.py               # Flask application
├── detect.py            # YOLO detection logic
├── models/
│   └── yolov8n.pt       # YOLOv8 model (lightweight)
├── templates/
│   └── index.html       # Web interface
└── README.md            # Project documentation
```

---

### 🚀 Getting Started

#### 1. Clone the repository

```bash
git clone https://github.com/roshanpandit65R/Real-Time-obstacles-Detection-on-road.git
cd folder path/
```

#### 2. Install required dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing, install manually:
```bash
pip install opencv-python flask pyttsx3 torch torchvision ultralytics
```

#### 3. Download YOLOv8n model

Make sure `yolov8n.pt` is present in the `models/` folder. You can download it from [Ultralytics YOLOv8 Releases](https://github.com/ultralytics/ultralytics/releases).

#### 4. Run the application

```bash
python app.py
```

#### 5. Open your browser

Go to: [http://localhost:5000](http://localhost:5000)

---

### ⚙️ How It Works

1. The webcam feed is passed through YOLOv8 for object detection.
2. For each detected object, the system estimates the distance.
3. If any object is closer than 500 cm:
   - Displays a warning: **"SLOW DOWN YOUR CAR!"**
   - Triggers a voice alert using `pyttsx3`.

---

### 📢 Voice Alert Demo

When an object (like a pedestrian, car, or truck) is detected too close to the camera, the system audibly says:

> “Slow down your car!”

---

### 📌 Notes

- Works best in daylight conditions with a clear camera view.
- You can adjust the **`focal_length`** or **`distance threshold`** for better accuracy.
- Ensure your system supports audio playback for `pyttsx3` to work correctly.

---

### 🙌 Credits

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [pyttsx3](https://pypi.org/project/pyttsx3/)

---

### 📃 License

This project is licensed under the **MIT License** – feel free to use, modify, and distribute.
