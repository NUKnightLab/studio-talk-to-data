from collections import defaultdict
import nltk


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


if __name__ == "__main__":
    s1 = "Preckwinkle's pet soda tax has been overthrown, what happens next?"
    s2 = "It had been weeks since Chicago had seen rain, so the wind-blown mist that tumbled out of the heather skies on October 11 felt like a cop-out for what should have poured down from the heavens."
    s3 = "Cook County Board President Toni Preckwinkle's sweetened beverage tax was sentenced to death at the tender age of two months old by a vote of 15 to 1 a day earlier."
    s4 = "One of the security guards, Mike DeVane, leaned over."
    s5 = "\"Were you here yesterday?\" the clean-cut, red faced, portly officer asked."


    s6 = "It had been weeks since Chicago had seen rain"
    s7 = "so the wind-blown mist that tumbled out of the heather skies on October 11 felt like a cop-out for what should have poured down from the heavens."

    scores = []
    scores.append(score_fact(s1))
    scores.append(score_fact(s2))
    scores.append(score_fact(s3))
    scores.append(score_fact(s4))
    scores.append(score_fact(s5))

    scores2 = []
    scores2.append(score_fact(s2))
    scores2.append(score_fact(s6))
    scores2.append(score_fact(s7))

    print(scores)
    #print(scores2)
