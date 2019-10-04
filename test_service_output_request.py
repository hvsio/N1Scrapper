from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.route('/upload', methods=['PUT'])
def on_put():
    my_dict = json.loads(request.get_data())
    print(my_dict)
    return jsonify({"status": "OKEY!"}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)
