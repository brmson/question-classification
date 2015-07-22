from sklearn import linear_model
from sklearn import svm
import gensim
import operator
import string
import random
import numpy as np

word_vector_path = "data/glove.6B.50d.bin"
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

def average_vector(dictionary, question):
    cnt = 0
    s = [0]*vector_dim
    for w in question.split(" "):
        w = w.lower()
        cnt += 1
        try:
            # print word, word_vector[word]
            s = map(operator.add, dictionary[w], s)
        except KeyError:
            # cnt -= 1
            # pass #Use random vector or skip?
            s = map(operator.add, dictionary.seeded_vector(random_generator(50)), s)
    if cnt == 0:
        return s
    return [elem/float(cnt) for elem in s]

def compute_accuracy(predicted, original):
    eq = [z[0] == z[1] for z in zip(predicted, original)]
    return eq.count(True)/float(len(eq))

def is_in_class(dictionary, questions, cls):
    model = linear_model.LogisticRegression()
    tr_lab = [x.split(":")[0] for x in train_labels]
    ts_lab = [x.split(":")[0] for x in test_labels]
    # print (tr_lab)
    # print np.array(tr_lab) == cls
    model.fit(questions, np.array(tr_lab) == cls)
    train_data_prediction = [model.predict(average_vector(dictionary, line[1].lower())) for line in train_data]
    test_data_prediction = [model.predict(average_vector(dictionary, line[1].lower())) for line in test_data]
    # for z in zip(train_data_prediction, np.array(lab) == cls):
    #     print z
    print "Train accuracy for class " + cls + ": " + str(compute_accuracy(train_data_prediction, np.array(tr_lab) == cls))
    print "Test accuracy for class " + cls + ": " + str(compute_accuracy(test_data_prediction, np.array(ts_lab) == cls))
    # print [model.predict(average_vector(dictionary, line[1].lower())) for line in train_data]
    # return [model.predict_proba(average_vector(dictionary, line[1].lower())) for line in train_data]


def get_closest_words(dictionary, question):
    vec = average_vector(dictionary, question)
    print vec
    return dictionary.most_similar(positive=[np.array(vec)])

if __name__ == "__main__":
    random.seed(12384523)
    gensim.utils.to_unicode = any2unicode
    word_vector = gensim.models.Word2Vec.load_word2vec_format(word_vector_path, binary=True)
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

    cfier = linear_model.LogisticRegression()
    cfier.fit(question_vectors, train_labels)
    train_data_prediction = [cfier.predict(average_vector(word_vector, line[1].lower())) for line in train_data]
    test_data_prediction = [cfier.predict(average_vector(word_vector, line[1].lower())) for line in test_data]
    # for z in zip(train_data_prediction, train_labels):
    #     print z
    print ("Accuracy with fine grained question classes:")
    print "Train accuracy " + str(compute_accuracy(train_data_prediction, train_labels))
    print "Test accuracy " + str(compute_accuracy(test_data_prediction, test_labels))
    print "Train accuracy for coarse class " + str(compute_accuracy([x[0].split(":")[0] for x in train_data_prediction],
                                                                    [x.split(":")[0] for x in train_labels]))
    print "Test accuracy for coarse class " + str(compute_accuracy([x[0].split(":")[0] for x in test_data_prediction],
                                                  [x.split(":")[0] for x in test_labels]))
    
    print ("Accuracy with coarse grained question classes:")
    cfier = linear_model.LogisticRegression(fit_intercept=True)
    coarse_test_labels = [line[0].split(":")[0] for line in test_data]
    coarse_train_labels = [line[0].split(":")[0] for line in train_data]
    cfier.fit(question_vectors, coarse_train_labels)
    train_data_prediction = [cfier.predict(average_vector(word_vector, line[1].lower())) for line in train_data]
    test_data_prediction = [cfier.predict(average_vector(word_vector, line[1].lower())) for line in test_data]
    print "Train accuracy " + str(compute_accuracy(train_data_prediction, coarse_train_labels))
    print "Test accuracy " + str(compute_accuracy(test_data_prediction, coarse_test_labels))
    for z in zip(train_data_prediction, coarse_train_labels):
        print z
    for line in train_data:
        print (line[1] + " " + str(get_closest_words(word_vector, line[1])))
    s = set()
    [s.add(elem) for elem in coarse_train_labels]
    # print is_in_class(word_vector, question_vectors, 'NUM')
    first = True
    for c in s:
        is_in_class(word_vector, question_vectors, c)



