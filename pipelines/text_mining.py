import numpy as np
import pandas as pd
from PAMI.frequentPattern.basic import FPGrowth
from PAMI.frequentPattern.basic import ECLAT
from utils.source import CATEGORIES, MAX_PART_SIZE, META_PARTS, METADATA_TYPE, PATH_CLEAR, PATH_TM, PATH_JSON, PATH_MERGE, PATH_OUT, PATH_SPM, PATH_SPM_OUT, REVIEWS_TYPE, job_dispatch_in_dataSource
import seaborn as sns
import matplotlib.pyplot as plt

all= CATEGORIES
done = []
dataSource=list(set(all) - set(done))
print(dataSource)


###############################
##          JOBS            ###
###############################

def job_extract_raw_reviews(i, source):
    df = pd.read_csv(PATH_CLEAR+source+"_cleared.csv",dtype=REVIEWS_TYPE)
    print("working on {} ({}/{})".format(source,i+1,len(dataSource)))
    # spm =df.loc[:,["reviewerID","asin","unixReviewTime","reviewText"]].sort_values(['unixReviewTime','reviewerID','asin'],ascending=False).groupby("reviewerID")['asin'].apply(list)
    df.loc[:,"reviewText"].to_csv(PATH_TM+source+".csv",index=False)
    print("done with {} ({}/{})".format(source,i+1,len(dataSource)))

# job_extract_raw_reviews(0, "Gift_Cards_5")


# df = pd.read_csv(PATH_TM+"Gift_Cards_5"+".csv")

def play_with_sens2vec():
    # https://github.com/facebookresearch/fastText
    # fast text fa il modello 
    # sense2vec ci lavora sopra 
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS
    stopwords=list(STOP_WORDS)
    from string import punctuation
    punctuation=punctuation+ '\n'
    nlp = spacy.load('en_core_web_sm')
    from sense2vec import Sense2VecComponent
    s2v = nlp.add_pipe("sense2vec")
    s2v.from_disk(PATH_TM)
    # The component will add several extension attributes and methods to spaCy's Token and Span objects 
    # that let you retrieve vectors and frequencies, as well as most similar terms.
    doc = nlp("A sentence about natural language processing.")
    assert doc[3:6].text == "natural language processing"
    freq = doc[3:6]._.s2v_freq
    vector = doc[3:6]._.s2v_vec
    most_similar = doc[3:6]._.s2v_most_similar(3)
    print(freq, vector, most_similar)

    # For entities, the entity labels are used as the "sense" (instead of the token's part-of-speech tag):
    doc = nlp("A sentence about Facebook and Google.")
    for ent in doc.ents:
        assert ent._.in_s2v
        most_similar = ent._.s2v_most_similar(3)
        print(ent.text, ent.label_, most_similar)

play_with_sens2vec()