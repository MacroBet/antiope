text="""The human coronavirus was first diagnosed in 1965 by Tyrrell and Bynoe from the respiratory tract sample of an adult with a common cold cultured on human embryonic trachea.1 Naming the virus is based on its crown-like appearance on its surface.2 Coronaviruses (CoVs) are a large family of viruses belonging to the Nidovirales order, which includes Coronaviridae, Arteriviridae, and Roniviridae families.3 Coronavirus contains an RNA genome and belongs to the Coronaviridae family.4 This virus is further subdivided into four groups, ie, the α, β, γ, and δ coronaviruses.5 α- and β-coronavirus can infect mammals, while γ- and δ- coronavirus tend to infect birds.6 Coronavirus in humans causes a range of disorders, from mild respiratory tract infections, such as the common cold to lethal infections, such as the severe acute respiratory syndrome (SARS), Middle East respiratory syndrome (MERS) and Coronavirus disease 2019 (COVID-19). The coronavirus first appeared in the form of severe acute respiratory syndrome coronavirus (SARS-CoV) in Guangdong province, China, in 20027 followed by Middle East respiratory syndrome coronavirus (MERS-CoV) isolated from the sputum of a 60-year-old man who presented symptoms of acute pneumonia and subsequent renal failure in Saudi Arabia in 2012.8 In December 2019, a β-coronavirus was discovered in Wuhan, China. The World Health Organization (WHO) has named the new disease as Coronavirus disease 2019 (COVID-19), and Coronavirus Study Group (CSG) of the International Committee has named it as SARS-CoV-2.9,10 Based on the results of sequencing and evolutionary analysis of the viral genome, bats appear to be responsible for transmitting the virus to humans"""

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
stopwords=list(STOP_WORDS)
from string import punctuation
punctuation=punctuation+ '\n'
nlp = spacy.load('en_core_web_sm')


# sense2vec https://github.com/explosion/sense2vec
def play_with_sens2vec():
    from sense2vec import Sense2VecComponent
    s2v = nlp.add_pipe("sense2vec")
    s2v.from_disk("/Volumes/Extreme SSD/data/csv/Gift_Cards_5.csv")
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

# similarity
def similarity():
    nlp = spacy.load("en_core_web_md")  # make sure to use larger package!
    doc1 = nlp("I like salty fries and hamburgers.")
    doc2 = nlp("Fast food tastes very good.")

    # Similarity of two documents
    print(doc1, "<->", doc2, doc1.similarity(doc2))
    # Similarity of tokens and spans
    french_fries = doc1[2:4]
    burgers = doc1[5]

    print(french_fries, "<->", burgers, french_fries.similarity(burgers))

# 1. text summarization https://www.numpyninja.com/post/text-summarization-through-use-of-spacy-library
def summarize():
    doc= nlp(text)
    tokens=[token.text for token in doc]
    print(tokens)
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    print(word_frequencies)

    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency

    print(word_frequencies)

    sentence_tokens= [sent for sent in doc.sents]
    print(sentence_tokens)

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]

    print(sentence_scores)

    from heapq import nlargest
    select_length=int(len(sentence_tokens)*0.3)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    print(final_summary)
    summary=''.join(final_summary)
    print("summary",summary)

# There can be various other ways like use of library nltk to do it by using lexical analysis,
# part of speech tagger and n-grams. We will talk more about it in my next blog.



# 5. sentiment analysis https://spacy.io/universe/project/spacy-textblob
# 6. textblob https://github.com/sloria/TextBlob

def play_with_blob():
    nlp.add_pipe('spacytextblob')
    doc = nlp(text)
    for sentence in doc._.blob.sentences:
        print(sentence.raw)
        print(sentence.sentiment.polarity)
    print(doc._.blob.polarity)                            # Polarity: -0.125
    print(doc._.blob.subjectivity)                        # Subjectivity: 0.9
    print(doc._.blob.sentiment_assessments.assessments)   # Assessments: [(['really', 'horrible'], -1.0, 1.0, None), (['worst', '!'], -1.0, 1.0, None), (['really', 'good'], 0.7, 0.6000000000000001, None), (['happy'], 0.8, 1.0, None)]
    doc._.blob.ngrams()  

def other_examples():

    # process several texts properly
    texts = ["This is a text", "These are lots of texts", "..."]
    docs = list(nlp.pipe(texts), n_process=4)


    # disable some parts of spaCy process
    texts = [
        "Net income was $9.4 million compared to the prior year of $2.7 million.",
        "Revenue exceeded twelve billion dollars, with a loss of $1b.",
    ]

    nlp = spacy.load("en_core_web_sm")
    for doc in nlp.pipe(texts, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):
        # Do something with the doc here
        print([(ent.text, ent.label_) for ent in doc.ents])

play_with_sens2vec()