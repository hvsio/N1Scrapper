from flask import Flask, request, jsonify
import json

app = Flask(__name__)
timeout = 15


@app.route('/upload', methods=['PUT'])
def on_put():
    my_dict = json.loads(request.get_data())
    print(my_dict)
    return jsonify({"status": "OKEY!"}), 201


@app.route('/timeout', methods=['GET'])
def on_get():
    try:
        return str(timeout), 200
    except:
        return jsonify({"status": "Getting timeout error"}), 408


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)
