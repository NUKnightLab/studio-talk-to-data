import sys
import csv

def parse_claim_data(dataset):
    """ Parses claim dataset and outputs a dictionary """
    with open(dataset, 'rb') as data:
        rows = csv.reader(data, delimiter = ",")
        try:
            claim_dict = { row[0].strip() : bool(row[1]) for row in rows if row[0] }
        except csv.Error as e:
            sys.exit('Error reading file %s at line %d: %s' % (filename, reader.line_num, e))
        return claim_dict