from flask import Flask, render_template, request
import base64
app = Flask(__name__)
import json

@app.route('/')
def hello_world():
    return render_template('hd.html')

@app.route('/file', methods=['POST'])
def write_file():
    img_data = request.form['jpg'].split(',')[1]
    img_data = bytes(img_data,encoding='ascii')
    with open("imageToSave.jpg", "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    return json.dumps("{}")
