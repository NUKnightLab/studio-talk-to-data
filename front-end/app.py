from flask import Flask, jsonify, abort, request, render_template
import requests
from werkzeug.utils import secure_filename

from nltk import word_tokenize, pos_tag

app = Flask(__name__)

#homepage of the site
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

#called when using the form on the homepage
@app.route('/upload', methods=['POST', 'GET'])
def color():

    class token_obj():

        def __init__(self, token, t=0):
            self.text = token
            self.type = t
            self.space = (self.text != '.' and self.text != ',')

    if request.method == 'POST':
        #try:
        f = request.files['article']

        contents = f.read().decode("utf-8")

        tagged = pos_tag(word_tokenize(contents))

        tokens = []


        for pair in tagged:
            if "NP" in pair[1]:
                tokens.append(token_obj(pair[0], 1))
            elif "CD" == pair[1]:
                tokens.append(token_obj(pair[0], 2))
            else:
                tokens.append(token_obj(pair[0], 0))

        return render_template('test.html', tokenized=tokens)
        #except:
        #    return render_template('error.html')
    else:
        return render_template('error.html')
