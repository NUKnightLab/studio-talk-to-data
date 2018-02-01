# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 09:00:38 2018

@author: Crystal Gong
"""
import nltk
from nltk.corpus import names
from nltk.classify import apply_features

import random
import pandas as pd
import spacy

nlp = spacy.load('en_core_web_sm')

import re

#####################

#returns final letter of given name 
def gender_features(word):
    return {'last_letter': word[-1]}


#########
"""
Parsing data sets
"""
# Takes a data set file and returns a dictionary
def file_to_dict(dataset):
    dic = pd.Series.from_csv(dataset, header=None).to_dict()
    return dic
# takes a string and divides it into sentences
def string_to_sentences(data):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return tokenizer.tokenize(data)  #get sentences
# for parsing the claim files 
def datafile_to_df(filename):
    df= pd.read_csv(filename, header=None) 
    return df
# returns a list of tuple from a file with one column of text and one column of text type
def file_to_tuple(filename):
    df= pd.read_csv(filename, header=None) 
    return [tuple(x) for x in df.to_records(index=False)]

# returns a list of tuple from a file with one column of POS and one column of text type
def file_to_pos_tuple(filename):
    df= pd.read_csv(filename, header=None) 
    df[0]=df[0].apply(get_tags)
    return [tuple(x) for x in df.to_records(index=False)]
"""
Getting tags
"""
# gets the tags of a string
def get_tags(sentence):
    tokens = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(tokens)
    return tags
# takes a string of the data and returns a dataframe with the
def get_tokens_chart(data):
    parsed_data = nlp(data)
    token_text = [token.orth_ for token in parsed_data] #TEXT
    token_pos = [token.pos_ for token in parsed_data] #POS
    token_lemma = [token.lemma_ for token in parsed_data] #LEMMA
    token_shape = [token.shape_ for token in parsed_data] #SHAPE

    return pd.DataFrame(list(zip(token_text, token_pos, token_lemma, token_shape)),
                 columns=['token_text', 'part_of_speech', "lemma", "shape"])

"""
Checking for entities

"""
#gets the entities of a string
def get_entities(sentence):
    entities = {}
    for num, entity in enumerate(nlp(sentence).ents):
        entities.update({entity: entity.label_})
        # entities.update({entity: entity.label}) #use to get the entities as abbreviations
    return entities
# prints entities
def print_entities(sentence):
    entities = get_entities(sentence)
    for entity in entities:
        print('Entity:', entity, '-', entities[entity]) 
#gets all the proper nouns of the string
def get_proper_nouns(sentence): ## still to be implemented
    tags = get_tags(sentence)
    proper_noun_list = []
    noun_part = ""
    for word, pos in tags:
        if pos == 'NNP':
            noun_part += word + ' ' 
            continue
        if len(noun_part) > 0:
            proper_noun_list.append(noun_part[:-1])
            noun_part = ""

    if len(noun_part) > 0:
        proper_noun_list.append(noun_part[:-1])
            
    return proper_noun_list
# gets all the dates to the string
def get_dates(sentence):
    return False

"""
Get quotes
"""

def get_quotes(sentence): #to be fixed
    m = re.search('([\"\'])(?:(?=(\\?))\2.)*?\1', sentence)
    return m.group(0)

if __name__ == "__main__":
    TRAIN_FILE = "data/claim_dataset.csv" #our training file #labeled_names
    TEST_FILE = "data/article.csv" #our testing file 
    labeled_set = file_to_tuple(TRAIN_FILE) #text, text type
    feature_set = file_to_pos_tuple(TRAIN_FILE) #POS, text type
    classifier = nltk.NaiveBayesClassifier.train(feature_set)
    print(classifier.classify(get_tags('I like cats')))
    """
#    labeled_names = ([(name, 'male') for name in names.words('male.txt')] + 
#                      [(name, 'female') for name in names.words('female.txt')])
#    random.shuffle(labeled_names)
    
    featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
    train_set, test_set = featuresets[500:], featuresets[:500]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    
    print(classifier.classify(gender_features('Neo')))
    print(classifier.classify(gender_features('Trinity')))
    print(nltk.classify.accuracy(classifier, test_set))
    print(classifier.show_most_informative_features(5))
    
    train_set = apply_features(gender_features, labeled_names[500:])
    test_set = apply_features(gender_features, labeled_names[:500])
    """
    
    #can try to find frequency of claim words
    # gensium
    # insert tags into sentence 
    
    my_sent = "WASHINGTON -- In the wake of a string of abuses by New York police officers in the 1990s, Loretta E. Lynch, the top federal prosecutor in Brooklyn, spoke forcefully about the pain of a broken trust that African-Americans felt and said the responsibility for repairing generations of miscommunication and mistrust fell to law enforcement."