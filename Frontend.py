from flask import Flask, jsonify, request
from flask_cors import CORS

class Frontend:

    def __init__ (self):
        self.is_connected = False
        self.app = Flask(__name__)
        CORS(self.app)
        self.app.run(debug=True)
        self.run_video = True

    def define_routed(self):
        @self.app.route('/api/data')
        def get_data():
            data = {
                'msg': 'Some message'
            }
            return jsonify(data)

        @self.app.route('/api/action', methods=['POST'])
        def perform_action():
            data = request.json
            is_checked = data.get('isChecked', False)
            # Perform some action based on the checkbox state
            self.run_video = is_checked
            if is_checked:
                result = "Action performed"
            else:
                result = "Action reversed"

            return jsonify({"result": result})


if __name__ == "__main__":
    myFrontend = Frontend()