from sklearn import linear_model
import gensim
import operator
import string
import random

word_vector_path = "data/glove.6B.50d.txt"
training_data_path = "data/train_5500.label"
testing_data_path = "data/TREC_10.label"
vector_dim = 50

def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def any2unicode(text, encoding='utf8', errors='strict'):
        """Convert a string (bytestring in `encoding` or unicode), to unicode."""
        if isinstance(text, unicode):
                return text
        return unicode(text.replace('\xc2\x85', '<newline>'), encoding, errors=errors)

def load_data(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            label, question = line.split(" ", 1)
            res.append((label, question))
    return res

def average_vector(vector, question):
    cnt = 0
    s = [0]*vector_dim
    for w in question[1].split(" "):
        w = w.lower()
        cnt += 1
        try:
            # print word, word_vector[word]
            s = map(operator.add, vector[w], s)
        except KeyError:
            cnt -= 1
            pass #Use random vector or skip?
            # s = map(operator.add, random_generator(50), s)
    if cnt == 0:
        return s
    return [x/cnt for x in s]

if __name__ == "__main__":
    random.seed(12384523)
    gensim.utils.to_unicode = any2unicode
    word_vector = gensim.models.Word2Vec.load_word2vec_format(word_vector_path, binary=False)
    # word_vector.save_word2vec_format("data/glove.6B.50d.bin", binary=True)
    train_data = load_data(training_data_path)
    test_data = load_data(testing_data_path)
    question_vectors = []
    train_labels = []
    test_labels = [line[0] for line in test_data]
    for line in train_data:
        train_labels.append(line[0])
        s_avg = average_vector(word_vector, line[1])
        question_vectors.append(s_avg)

    cfier = linear_model.LogisticRegression(fit_intercept=False)
    cfier.fit(question_vectors, train_labels)
    train_data_prediction = [cfier.predict(average_vector(word_vector, line[1].lower())) for line in train_data]
    test_data_prediction = [cfier.predict(average_vector(word_vector, line[1].lower())) for line in test_data]
    for z in zip(train_data_prediction, train_labels):
        print z
    eq = [z[0] == z[1] for z in zip(train_data_prediction, train_labels)]
    accuracy = eq.count(True)/float(len(eq))
    print "Train accuracy " + str(accuracy)
    eq = [z[0] == z[1] for z in zip(test_data_prediction, test_labels)]
    accuracy = eq.count(True)/float(len(eq))
    print "Test accuracy " + str(accuracy)
    print(word_vector.most_similar("usa"))



