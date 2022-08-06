from gensim.models import KeyedVectors
# load the Stanford GloVe model
filename = '/Volumes/Extreme SSD/data/trained/glove.6B/glove.6B.100d.txt.word2vec'
model = KeyedVectors.load_word2vec_format(filename, binary=False)
# calculate: (king - man) + woman = ?
result = model.most_similar(positive=['woman', 'king'], negative=['man'], topn=1)
print(result)


# from gensim.scripts.glove2word2vec import glove2word2vec
# glove_input_file = '/Volumes/Extreme SSD/data/trained/glove.6B/glove.6B.100d.txt'
# word2vec_output_file = '/Volumes/Extreme SSD/data/trained/glove.6B/glove.6B.100d.txt.word2vec'
# glove2word2vec(glove_input_file, word2vec_output_file)