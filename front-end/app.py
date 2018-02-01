from flask import Flask, jsonify, abort, request, render_template
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['article']

        f_name = secure_filename(f.filename)
        return f.read()
        #return render_template('uploaded.html')
