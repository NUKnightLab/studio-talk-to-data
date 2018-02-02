from flask import Flask, jsonify, abort, request, render_template

from nltk import word_tokenize, pos_tag

app = Flask(__name__)

#homepage of the site
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

#called when using the form on the homepage
@app.route('/upload', methods=['POST', 'GET'])
def color():

    #class to wrap around tokens for easier use in jinja templates (highlighting)
    class token_obj():
        def __init__(self, token, t=0):
            self.text = token
            self.type = t

    #class to wrap around tokens for use in jinja templates (list of facts by type)
    class token_list():
        def __init__(self, token, number):
            self.number = number
            self.token = token

    if request.method == 'POST':
        #try:
        #get uploaded file
        f = request.files['article']
        #convert to utf-8 string
        contents = f.read().decode("utf-8")
        #get part of speech tags
        tagged = pos_tag(word_tokenize(contents))

        #initialize variables used in the for loop
        tokens = []
        nouns = []
        numbers = []
        token = ''
        color_code = 0

        nouns_count = 1
        numbers_count = 1

        #iterate through token, tag pairs
        for i in range(len(tagged)):
            pair = tagged[i]
            token += pair[0]
            tag = pair[1]

            #proper noun
            if "NP" in tag:
                color_code = 1
                if i != len(tagged) - 1 and ("NP" in tagged[i+1][1] or tagged[i+1][1] == "POS"):
                    if tagged[i+1][0].isalpha():
                        token += ' '
                    continue
                tokens.append(token_obj(token, color_code))
                nouns.append(token_list(token, nouns_count))
                nouns_count += 1
                token = ''
                color_code = 0

            #number (cardinal digit)
            elif "CD" == tag:
                color_code = 2
                tokens.append(token_obj(token, color_code))
                numbers.append(token_list(token, numbers_count))
                numbers_count += 1
                token = ''
                color_code = 0
            else:
                if token == "``" or token == "''":
                    token = "\""
                tokens.append(token_obj(token, color_code))
                if color_code == 1:
                    nouns.append(token_list(token, nouns_count))
                    nouns_count += 1
                elif color_code == 2:
                    numbers.append(token_list(token, numbers_count))
                    numberss_count += 1
                token = ''
                color_code = 0

        return render_template('uploaded.html', tokenized=tokens, nouns=nouns, numbers=numbers)
        #except:
        #    return render_template('error.html')
    else:
        return render_template('error.html')
