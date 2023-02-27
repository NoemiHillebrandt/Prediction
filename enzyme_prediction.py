
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import pickle
from feature_generation import *


def check_for_AA_sequence(ref_seq):
    #Returns error if sequence looks like DNA instead of AA
    if "M" in ref_seq or "S" in ref_seq or "m" in ref_seq or "s" in ref_seq:
        print ("")
    else:
        print (f'You might have inserted a DNA sequence!')

def enzyme_calculation (seq_record):
    '''
    Function with input of sequence that returns enzyme

    Parameters
    ----------
    seq_record : sequence of enzyme of interest

    Returns
    -------
    enzyme type
    '''
    include_charge_features=False
    #fill in filenames here!
    used_classifier="Classifier/fill in something" # hier werden die all_enzyme_files eingefügt
    filename_permutations="permutations.txt"
    with open(filename_permutations, 'r') as file:
        permutations = [line.rstrip('\n') for line in file]
    check_for_AA_sequence(seq_record)
    #create a fake fragment matrix for enzyme prediction
    seq_record=SeqRecord(Seq(seq_record),id="sequence of interest")
    fragment_matrix=pd.DataFrame()
    new_row= {"whole_enzyme":seq_record.seq}
    fragment_matrix=fragment_matrix.append(new_row, ignore_index=True)
    feature_matrix=featurize(fragment_matrix, permutations, ["whole_enzyme"], include_charge_features)
    classifier = pickle.load(open(used_classifier, 'rb'))
    #predict enzyme
    predicted_enzyme=classifier.predict(feature_matrix)
    y_score = classifier.predict_proba(feature_matrix)
    return (predicted_enzyme)
