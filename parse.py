import sys
import csv
import pandas as pd

def parse_claim_data2(dataset):
    """ Parses claim dataset and outputs a dictionary """
    with open(dataset, 'rb') as data:
        rows = csv.reader(data, delimiter = ",")
        try:
            claim_dict = { row[0].strip() : bool(row[1]) for row in rows if row[0] }
        except csv.Error as e:
            sys.exit('Error reading file %s at line %d: %s' % (dataset, rows.line_num, e))
        return claim_dict
    
def parse_claim_data(dataset):
    """ Fix errors with reading by using pandas """
    dic = pd.Series.from_csv(dataset, header=None).to_dict()
    return dic
