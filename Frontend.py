import sys
import time

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from threading import Thread
import cv2
from frame import Frame
from urllib.parse import urlparse, parse_qs

class Frontend:
    frame: Frame = None
    frame_has_changed = False
    demand_stream_stop = False
    running_streams = []

    def __init__(self):
        self.is_connected = False
        self.app = Flask(__name__)
        CORS(self.app)
        self.run_video = True
        self.define_routes()
        self.start_flask_thread()
        self.stream_to_stop = 0

    def update_frame(self, frame: Frame):
        self.frame = frame
        self.frame_has_changed = True

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
            stream_already_running = False
            url = request.url
            parsed_url = urlparse(url)
            params = parse_qs(parsed_url.query)
            params = {k: v[0] if v else None for k, v in params.items()}#remove the lists that are present by default
            stream_is_running = any(params["stream_ID"] == x["stream_ID"] for x in self.running_streams)
            if stream_is_running:
                if params not in self.running_streams:
                    print("detected change of parameter")
                    self.stop_stream_by_ID(params["stream_ID"])
                    self.running_streams.append(params)
                else:
                    stream_already_running = True
                    print("stream is running already")
            else:
                print("stream was not running")
                self.running_streams.append(params)
            if not stream_already_running:
                frame = self.generate_frames(filter=params['filter'],
                                             with_rows=params['with_rows']=='with_rows',
                                             with_level=params['with_level']=='with_level',
                                             stream_ID=params['stream_ID'])
                return Response(frame,
                                mimetype='multipart/x-mixed-replace; boundary=frame')


        @self.app.route('/stop_stream')
        def stop_stream():
            return self.stop_stream_by_ID(int(request.args.get('stream_ID')))

    def generate_frames(self, filter, with_rows, with_level, stream_ID):
        while True:
            while not self.frame_has_changed:
                pass
            if self.demand_stream_stop and stream_ID == self.stream_to_stop:
                print(f"stopped stream {stream_ID}")
                self.demand_stream_stop = False
                break
            self.frame_has_changed = True
            frame = self.frame.get_frame(filter=filter, with_rows=with_rows, with_level=with_level)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            print("streaming...")
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def stop_stream_by_ID(self, stream_ID):
        if self.demand_stream_stop:
            print("waiting for stream stop")
            time.sleep(1)
        self.stream_to_stop = stream_ID
        self.demand_stream_stop = True
        time.sleep(1)
        self.running_streams = list(filter(lambda d: d.get('stream_ID') != stream_ID, self.running_streams))
        if self.demand_stream_stop:
            self.demand_stream_stop = False
            return jsonify({'msg': f'stream {self.stream_to_stop} was not running'})
        else:
            return jsonify({'msg': f'stream {self.stream_to_stop} was stopped'})

if __name__ == "__main__":
    myFrontend = Frontend()