from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/api/data')
def get_data():
    data = {
        'msg': 'Some message'
    }
    return jsonify(data)


@app.route('/api/action', methods=['POST'])
def perform_action():
    data = request.json
    is_checked = data.get('isChecked', False)
    # Perform some action based on the checkbox state
    if is_checked:
        result = "Action performed"
    else:
        result = "Action reversed"

    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)