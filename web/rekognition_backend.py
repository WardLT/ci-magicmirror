from flask import Flask, render_template, request
import base64
app = Flask(__name__)
import json
import pickle

@app.route('/')
def hello_world():
    return render_template('hd.html')

@app.route('/file', methods=['POST'])
def write_file():
    img_data = request.form['jpg'].split(',')[1]
    img_data = bytes(img_data,encoding='ascii')
    with open("imageToSave.jpg", "rb") as fh:
        f = fh.read()
        pickle.dump(bytearray(f), open("imageToSave.bytearray", 'w'))
    return json.dumps("{}")
