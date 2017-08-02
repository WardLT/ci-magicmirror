from flask import Flask, render_template, request
import base64
app = Flask(__name__)
import json
import boto3
import index_and_search as ins

@app.route('/')
def hello_world():
    return render_template('hd.html')

@app.route('/file', methods=['POST'])
def write_file():
    img_data = request.form['jpg'].split(',')[1]
    img_data = bytes(img_data,encoding='ascii')
    with open("imageToSave.jpg", "wb") as fh:
        fh.write(base64.decodebytes(img_data))
    with open("imageToSave.jpg", 'rb') as img:
        img_data = bytearray(img.read())
    response = ins.search_image(img_data, collection_name='ci-faces', bucket_name = 'ci-magicmirror', method='byte')
    #print(response.keys())
    print(ins.get_names(response['FaceMatches'][0]['Face']['ExternalImageId']))
    return json.dumps("{}")
