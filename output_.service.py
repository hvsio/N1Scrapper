from flask import Flask, request, jsonify
import json

app = Flask(__name__)
timeout = 15


@app.route('/upload', methods=['POST'])
def on_post():
    my_dict = json.loads(request.get_data())
    print(my_dict)
    return jsonify({"status": "OKEY!"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)
    #app.run(host='0.0.0.0')
