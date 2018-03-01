from nltk import word_tokenize, pos_tag


NOUN = 1
QUOTE = 2
NUMBER = 3


def get_all_claims(article):
    """
    Take an article process it into claims.

    Input:
        dictionary
    Output:
        list of dictionary

    Process the given article into a list of claim dictionaries that can be placed
    into the database or sent to the front end
    """
    #get tags
    tagged = pos_tag(word_tokenize(article['text']))
    #initialize variables
    claims = []
    total_length = 0
    num_tags = len(tagged)
    i = 0

    claim_text = None
    current_length = 0

    #iterate through the list of paired tag
    while i < num_tags:
        #proper noun
        if 'NNP' in tagged[i][1]:
            claim_text = tagged[i][0]
            current_length = total_length
            current_length += len(tagged[i][0]) + 1
            i += 1
            #treat adjacent proper nouns as one claim
            while 'NNP' in tagged[i][1] or 'POS' == tagged[i][1]:
                if 'POS' == tagged[i][1]:
                    current_length += len(tagged[i][0])
                else:
                    current_length += len(tagged[i][0]) + 1
                    claim_text += ' '
                claim_text += tagged[i][0]
                i += 1
            new_claim = {'article_id': article['id'],
                        'text': claim_text,
                        'claim_type': NOUN,
                        'start_index': total_length,
                        }
            claims.append(new_claim)
            total_length = current_length
        #number
        elif 'CD' == tagged[i][1]:
            new_claim = {'article_id': article['id'],
                        'text': tagged[i][0],
                        'claim_type': NUMBER,
                        'start_index': total_length,
                        }
            claims.append(new_claim)
            total_length += len(tagged[i][0]) + 1
            i += 1
        #quote
        elif '``' == tagged[i][1]:
            claim_text = '"'
            current_length = total_length
            current_length += 1
            i += 1
            while tagged[i][1] != "''" and i < num_tags:
                current_length += len(tagged[i][0])
                claim_text += tagged[i][0]
                if tagged[i][0].isalnum():
                    current_length += 1
                    claim_text += ' '
                i += 1
            claim_text = claim_text[:-1] + '"'
            current_length += 1
            i += 1

            new_claim = {'article_id': article['id'],
                        'text': claim_text,
                        'claim_type': QUOTE,
                        'start_index': total_length,
                        }
            claims.append(new_claim)
            total_length = current_length

        else:
            total_length += len(tagged[i][0])
            if tagged[i][0].isalnum():
                total_length += 1
            i += 1


    return claims



def filter_claims(claims, type_id):
    """
    Return list of claims filtered by claim type.

    Input:
        list of dictionary, integer
    Output:
        list of dictionary
    """
    #select only claims that have the correct claim_type
    return list(filter(lambda x: x[claim_type] == type_id))



if __name__ == '__main__':
    test = 'The White House is "actively considering issuing a veto threat" against the 51 to 49 House vote.'
    print('\n')
    claims = get_all_claims({'text': test, 'id': 1})
    print(claims)
    print('\n\n')
    for claim in claims:
        print(test[claim['start_index']:claim['start_index']+ len(claim['text'])])
