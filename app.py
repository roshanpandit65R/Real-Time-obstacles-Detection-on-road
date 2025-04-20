from flask import Flask, render_template, Response, jsonify
from detect import detect_objects, detected_alert  # Ensure detect.py is correctly imported

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(detect_objects(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alert_status')
def alert_status():
    return jsonify({"alert": detected_alert})

if __name__ == '__main__':  # ✅ Fixed '__main__' typo
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)  # ✅ Added threaded=True for better performance
