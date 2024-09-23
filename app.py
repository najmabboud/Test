# from flask import Flask, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)

import cv2

def open_camera():
    # فتح الكاميرا
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # قراءة الإطار من الكاميرا
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            break

        # عرض الإطار
        cv2.imshow('Camera', frame)

        # إنهاء الحلقة عند الضغط على 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # تحرير الكاميرا وإغلاق النوافذ
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    open_camera()
