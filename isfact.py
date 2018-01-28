from collections import defaultdict
from parse import parse_claim_data
import nltk
import pandas as pd

import en_core_web_sm
nlp = en_core_web_sm.load()

def trim_tokens(tokens):
    """
    removes non alpha numeric tags
    """

    for i in list(range(len(tokens)))[::-1]:
        if not tokens[i].isalnum():
            del tokens[i]

    return tokens


def score_fact(sentence):
    """
    Give an numerical rating of likelihood of being a fact.

    Input:
        string
    Output:
        integer > 0
    """

    #start score at 0
    score = 0
    #make a dictionary mapping pos tags to point values
    score_map_pos = make_point_map_pos()
    score_map_word = make_score_map_word()


    tokens = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(tokens)

    for pair in tags:
        score += score_map_word[pair[0]]
        score += score_map_pos[pair[1]]
        #print(pair[0], score)

    score /= len(trim_tokens(tokens))

    return score


def make_point_map_pos():
    """
    Initialize a dictionary that maps pos tags to point values.

    Input:
        None
    Output:
        dictionary

    Note: All values are arbitrary.
    """
    score_map = defaultdict(int)
    #quotes
    score_map["``"] = 20

    #proper nouns
    score_map["NNP"] = 8
    score_map["NNPS"] = 8

    #numbers
    score_map["CD"] = 5

    #foreign words
    score_map["FW"] = 3

    #strong language
    score_map["!"] = 3
    score_map["RB"] = 1
    score_map["RBR"] = 1
    score_map["RBS"] = 1
    score_map["JJ"] = 1
    score_map["JJR"] = 1
    score_map["JJS"] = 1

    #time
    #todo not yet implemented

    return score_map


def make_score_map_word():
    """
    Initialize a dictionary that maps specific words to point values.

    Input:
        None
    Output:
        dictionary

    Note: All values are arbitrary.
    """

    score_map = defaultdict(int)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_abrv = ['Jan', 'Feb', 'March', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    other_temporal = ['year', 'month', 'day', 'week', 'hour', 'minute', 'second']

    indicating_speech = ['said', 'says', 'stated']

    for month in months:
        score_map[month] = 5
    for abrv in month_abrv:
        score_map[abrv] = 5
    for other in other_temporal:
        score_map[other] = 3
    for word in indicating_speech:
        score_map[word] = 8


    return score_map

# takes the claims dictionary and creates a map with text (key) and scores (value)
def claims_to_scores_dict(claim_dict):
    claim_scores = {} #hashmap of scores and claims
    for key, value in claim_dict.items():
        score = score_fact(key)
        claim_scores.update({score: value})

# takes the claims dictionary and creates a dataframe with the text, true/false fact, and score       
def claims_to_scores_df(claim_dict):
    claim_df = pd.DataFrame(columns=["text", "is_fact", "score"])
    index = 0
    for key, value in claim_dict.items():
        score = score_fact(key)
        claim_df.loc[index] = [key, value, score]
        index += 1
    
#takes a string of the entire article and breaks it down into sentences
def data_to_sentences(data_all):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return tokenizer.tokenize(data_all)  #get sentences

#gets the entities of a string
def print_entities(sentence):
    for num, entity in enumerate(nlp(sentence).ents):
        print('Entity ():'.format(num + 1), entity, '-', entity.label_)
        print('')  
        
def get_entities(sentence):
    entities = {}
    for num, entity in enumerate(nlp(sentence).ents):
        entities.update({entity: entity.label})
    return entities

# takes a string of the data and returns a dataframe with the
def get_tokens_chart(data):
    parsed_data = nlp(data_all)
    token_text = [token.orth_ for token in parsed_data] #TEXT
    token_pos = [token.pos_ for token in parsed_data] #POS
    token_lemma = [token.lemma_ for token in parsed_data] #LEMMA
    token_shape = [token.shape_ for token in parsed_data] #SHAPE

    return pd.DataFrame(list(zip(token_text, token_pos, token_lemma, token_shape)),
                 columns=['token_text', 'part_of_speech', "lemma", "shape"])

# gets the POS tags of a sentence 
def get_tags(sentence):
    tokens = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(tokens)
    return tags

# gets quotes from data
def get_quotes(data):
    grammar = r'"', " '' "
    tags = get_tags(data)
    cp = nltk.RegexpParser(grammar) 
    return cp.parse(tags) 

if __name__ == "__main__":
    """
    To Do:
    https://spacy.io/usage/linguistic-features
    http://nlpforhackers.io/training-pos-tagger/
    implement function to get quotes or check if something is a quote
    implement something with entities --> all sentences with entities should be checked
    implement training system based on claims file 
    """
    CLAIM_TEST_DATA_FILE = "data/claim_dataset.csv" #our claims csv
    CLAIM_OUT_FILE = "data/claim_scores.csv" #csv to store scoring of the claims
    TEXT_FILE = 'data/article.csv' #csv to store claims
    """
    claim_dict = parse_claim_data(CLAIM_TEST_DATA_FILE) #make a dict from claims file
    claim_df = claims_to_scores_df(claim_dict)
    """
    # assumption: articles stores as columns of csv
    data = pd.read_csv(TEXT_FILE, header=None) #read data file
    data_all = data[0][:].str.cat(sep=' ') #concatenate all cols into one string

    sentences = data_to_sentences(data_all)  #get sentences
    scores=[]
    for s in sentences:
        scores.append(score_fact(s))
        print(s)
        print_entities(s)
        
    # tokens = get_tokens_chart(data_all)
    # claim_df.to_csv(CLAIM_OUT_FILE, sep='\t')
    

    
