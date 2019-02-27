import warnings
from asl_data import SinglesData

# SinglesData
# the object is type SinglesData
# the internal dictionary keys are the index of the test word rather than the word itself
# the getter methods are get_all_sequences, get_all_Xlengths, get_item_sequences and get_item_Xlengths


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

     :param models: dict of trained models
         {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
     :param test_set: SinglesData object
     :return: (list, list)  as probabilities, guesses
         both lists are ordered by the test set word_id
         - probabilities is a list of dictionaries where each key a word and value is Log Liklihood
             [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
              {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
             ]
         - guesses is a list of the best guess words ordered by the test set word_id
             ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
     """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []

    for word_id, word_xlengths in test_set.get_all_Xlengths().items():
        word_x, word_lengths = word_xlengths[0], word_xlengths[1]
        
        probabilities.append({})
        for word, model in models.items():
            try:
                logL = model.score(word_x, word_lengths)
                probabilities[word_id][word] = logL
            except:
              probabilities[word_id][word] = float('-Inf')
              # print("couln't score for word {} using model {}".format(word, model.__class__.__name__))
    
    for words in probabilities:
        guess = max(words, key=words.get)
        guesses.append(guess)

    return probabilities, guesses


