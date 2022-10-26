text="""
Players of different range and different price, in the possible surprises we insert the players who inspire confidence and can be good shots. Spotlight on Abdelhamid Sabiri: in view of the auction it is a very tempting and increasingly expensive bet, given that he is also one of the penalty takers. Arriving at Sampdoria at the end of last January, the former Ascoli had a great impact with Serie A. Season finale with good numbers: 11 appearances and three goals. Attacking midfielder who often goes to the conclusion. He has a deadly right, especially from long range. He is a bonus pawn and in fantasy football he can become a winning ace. He remains to be taken despite the increase in the price, which has not, however, spiked after the first few days. Yacine Adli is a new face of Milan. He is particularly expected because in the preseason he did well, but he has not yet had space in the league. In Bordeaux he showed important qualities and ample room for growth. At 21 he has 100 appearances and six goals in Ligue 1. he has dribbling, vision of the game and is a midfielder who will be very useful to Pioli in the trocar. Especially in the rotations, considering the many commitments of the Rossoneri season. However, he is not one of many goals, he is more of an assist. For example, compared to Sabiri the price is totally different, Adli is from the latest slots. Strefezza is a midfielder but plays in the attacking trident of Lecce, he comes from a season with 14 goals in 35 Serie B matches. Important numbers, which make him the classic possible surprise from Serie B as last year were Bajrami and Aramu. He can have that kind of path, clearly the double figures in Serie A are much more difficult. But if only he scored 50% of the goals he scored last year, he would be a super blow to fantasy football. He can be worth at least 5-10 fantamilioni, the price remains quite high because of the goal in the Italian Cup. Thorstvedt is Sassuolo's bet from abroad. Dionisi intends to play with the 4-3-3 and this favors him, he can be the starting midfielder but the place is played with Matheus Henrique. He may not be untouchable right away, but he is a level player, arrived from Genk and with international experience. One meter and 89 tall, he has an imposing physique (a la Pobega style) but also excellent technique, he can do both the attacking midfielder and the mezzala. Last season 5 goals in the league and one in the playoffs. He is cheap, he is a low cost from the latest slots. Ederson was a big surprise in last year's second round. With Salernitana he did well, also from the point of view of realization (two goals in 15 appearances). He has quality, offensive insertions and from a physical point of view he is a player who can make a difference. There are no regular players at Atalanta, but Ederson had done well in the preseason and Gasperini tried him out on the frontline. A path to become not only a quantity midfielder, but also a bonus. The price did not go up due to the injury he had at the beginning of the season. Vlasic comes to Turin to relaunch, he has disappointed twice in the Premier League - at West Ham and Everton - but he had done very well in Russia with CSKA Moscow. With Juric the attacking midfielders are exalted, the place will be played with Radonjic and Miranchuk (there are three for two places, those who have not played from the start take over and now the Russian is injured). He bet that he can be a winner if he has continuity. Radonjic could cost a little more after the sprint start. He is a typically attacking midfielder: he is a pawn that can be very useful to Juric. In recent years he has not shone as a continuity of performance due to several physical hiccups. But he is already back the one seen in 2019-2020 in Ligue 1 in Marseille (5 goals in 21 appearances), perhaps even better. He can become a surprise capable of bringing bonuses, including goals and assists. Juric effect.
"""

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
    # print(tokens)
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    # print(word_frequencies)

    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency

    # print(word_frequencies)

    sentence_tokens= [sent for sent in doc.sents]
    # print(sentence_tokens)

    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]

    # print(sentence_scores)

    from heapq import nlargest
    select_length=int(len(sentence_tokens)*0.1)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    # print(final_summary)
    summary=''.join(final_summary)
    print("Summary:\n",summary)

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

# play_with_sens2vec()

summarize()