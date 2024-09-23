from flask import Flask, request, render_template_string, send_from_directory
import os
import cv2
import mediapipe as mp
import threading
import numpy as np
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast,POINTER

wcam = 1280
hcam = 780

cap = cv2.VideoCapture(1)  # تأكد من استخدام الكاميرا الصحيحة
cap.set(3, wcam)
cap.set(4, hcam)

# إعداد Mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# إعداد الصوت
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volrange = volume.GetVolumeRange()
minvol = volrange[0]
maxvol = volrange[1]

# متغيرات للتحكم في الصوت
vol = 0
volbar = 400
volbarr = 0
camera_running = False
app = Flask(__name__)
def control_volume():
    global camera_running
    while camera_running:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        lmList = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                    
                if len(lmList) == 21:
                    x1, y1 = lmList[4][1], lmList[4][2]  # إبهام
                    x2, y2 = lmList[8][1], lmList[8][2]  # سبابة
                    
                    length = math.hypot(x2 - x1, y2 - y1)
                    vol = np.interp(length, [50, 200], [minvol, maxvol])
                    volbar = np.interp(length, [50, 300], [400, 150])
                    volbarr = np.interp(length, [50, 300], [0, 100])
                    volume.SetMasterVolumeLevel(vol, None)

                    # رسم مستطيل الصوت
                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    cv2.rectangle(img, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, f'{int(volbarr)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow('Hand Tracker', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

@app.route('/', methods=['GET', 'POST'])
def index():
    global camera_running
    music_files = []
    music_path = ""

    if request.method == 'POST':
        music_path = request.form['music_path'].strip()
        if os.path.isdir(music_path):
            music_files = [f for f in os.listdir(music_path) if f.endswith(('.mp3', '.wav', '.ogg'))]
            if music_files:
                camera_running = True
                threading.Thread(target=control_volume).start()
        else:
            music_files = ["Invalid directory"]

    return render_template_string('''
    <!doctype html>
    <html>
    <head>
        <title>Music File Loader</title>
    </head>
    <body>
        <h1>Music File Loader</h1>
        <form method="post">
            <label for="music_path">Enter Music Folder Path:</label>
            <input type="text" id="music_path" name="music_path" value="{{ music_path }}" required>
            <input type="submit" value="Load Music">
        </form>
        <h2>Music Files:</h2>
        <ul>
            {% for file in music_files %}
                <li>
                    {{ file }} 
                    <audio controls>
                        <source src="{{ url_for('serve_music', filename=file, path=music_path) }}" type="audio/mpeg">
                        Your browser does not support the audio tag.
                    </audio>
                </li>
            {% endfor %}
        </ul>
    </body>
    </html>
    ''', music_files=music_files, music_path=music_path)

@app.route('/music/<path:path>/<filename>')
def serve_music(path, filename):
    return send_from_directory(path, filename)

if __name__ == '__main__':
    app.run(debug=True)
