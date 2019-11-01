import subprocess
import sys
import threading
from datetime import datetime
from flask import Flask, request, jsonify
import go_spider

# Running subprocess in python:
# https://docs.python.org/3/library/subprocess.html

app = Flask(__name__)


@app.route('/scrapper', methods=['GET'])
def on_get():
    try:
        print(f'Starting new scrapping session at {datetime.now()}... ')

        try:
            t1 = threading.Thread(target=scrapp(), args=[])
            t1.start()
        except:
            print("Error: unable to start thread")
            return jsonify({"status": "Couldn't start scrapping"}), 500

        return jsonify({"status": "Starting scrapper"}), 200
    except:
        return jsonify({"status": "Getting timeout error"}), 408


def scrapp():
    print("Thread started!")
    # creating subprocess to run scrapper
    proc = subprocess.Popen([sys.executable, 'go_spider.py'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    # to display sys.out from subprocess
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        # the real code does filtering here
        print("SCRAPPER:", line.rstrip())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)
