import cv2
import torch
import numpy as np
import time
from ultralytics import YOLO
import pyttsx3

# Load YOLOv8 model
model = YOLO("models/yolov8n.pt")

# Initialize text-to-speech engine
tts_engine = pyttsx3.init()
# Set female voice if available
voices = tts_engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower():
        tts_engine.setProperty('voice', voice.id)
        break

# Global variables for detection data
detected_objects_data = {
    "objects": [],
    "closest_distance": None,
    "alert": False,
    "alert_message": None,
    "system_status": "Normal",
    "continuous_alert": False  # New flag for continuous alert state
}

def estimate_distance(bbox):
    _, _, width, height = bbox
    focal_length = 900
    real_object_width = 50
    distance = (real_object_width * focal_length) / width
    return round(distance, 2)

def speak_alert(message):
    try:
        tts_engine.say(message)
        tts_engine.runAndWait()
    except Exception as e:
        print(f"Error in text-to-speech: {e}")

def detect_objects():
    global detected_objects_data
    cap = cv2.VideoCapture(0)
    alert_active = False
    last_alert_time = 0
    alert_interval = 1.5  # seconds between repeat alerts (reduced from 3)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        results = model(frame)
        current_objects = []
        closest_distance = None
        alert_triggered = False
        current_time = time.time()

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                # Estimate distance
                distance = estimate_distance((x1, y1, x2 - x1, y2 - y1))
                
                # Track closest distance
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance

                # Add to current objects
                current_objects.append({
                    "name": class_name,
                    "distance": distance,
                    "confidence": confidence
                })

                # Draw bounding box and text
                label = f"{class_name} ({distance} cm)"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Check if object is too close
                if distance < 100:
                    cv2.putText(frame, "SLOW DOWN YOUR CAR!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    alert_triggered = True

        # Update global detection data
        detected_objects_data["objects"] = current_objects
        detected_objects_data["closest_distance"] = closest_distance
        detected_objects_data["alert"] = alert_triggered
        detected_objects_data["continuous_alert"] = alert_triggered  # Set continuous flag
        
        # Set system status and alert message
        if alert_triggered:
            detected_objects_data["system_status"] = "WARNING: Object too close!"
            detected_objects_data["alert_message"] = "Warning! Object too close. Slow down!"
            
            # Speak alert continuously while object is close
            if (current_time - last_alert_time) > alert_interval:
                speak_alert(detected_objects_data["alert_message"])
                last_alert_time = current_time
        else:
            detected_objects_data["system_status"] = "All systems normal" if closest_distance is None or closest_distance >= 200 else "Caution: Object nearby"
            detected_objects_data["alert_message"] = None
            detected_objects_data["continuous_alert"] = False

        # Encode frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()