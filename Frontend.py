import sys

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from threading import Thread
import cv2
from frame import Frame

class Frontend:
    frame: Frame = None
    def __init__(self):
        self.is_connected = False
        self.app = Flask(__name__)
        CORS(self.app)
        self.run_video = True
        self.define_routes()
        self.start_flask_thread()

    def update_frame(self, frame: Frame):
        self.frame = frame

    def start_flask_thread(self):
        flask_thread = Thread(target=self.run_flask)
        flask_thread.daemon = True
        flask_thread.start()

    def run_flask(self):
        self.app.run(debug=False, threaded=True)

    def define_routes(self):
        @self.app.route('/api/data')
        def get_data():
            data = {
                'msg': 'Burger Cam'
            }
            return jsonify(data)

        @self.app.route('/api/action', methods=['POST', 'OPTIONS'])
        def perform_action():
            if request.method == 'OPTIONS':
                return '', 200
            data = request.json
            is_checked = data.get('isChecked', False)
            self.run_video = is_checked
            if is_checked:
                print("running video")
            else:
                print("stopping video")
            return jsonify({"result": is_checked})

        @self.app.route('/video_feed')
        def video_feed():
            print("jup")
            filter = request.args.get('filter')
            frame = self.generate_frames(filter=filter)
            return Response(frame,
                            mimetype='multipart/x-mixed-replace; boundary=frame')


    def generate_frames(self, filter):
        while True:
            frame = self.frame.get_frame(filter=filter)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


    def generate_frames_old(self):
        camera = cv2.VideoCapture(r"D:\Videos Burger Wback\video 10.avi")  # Use 0 for webcam, or file path for video file
        while True:
            success, frame = camera.read()
            if not success or not self.run_video:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        camera.release()

if __name__ == "__main__":
    myFrontend = Frontend()