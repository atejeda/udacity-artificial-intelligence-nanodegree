import sys

import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences

class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None

class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)

class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    
    logL = likelihood, which is the model.score(X, lengths)
    N = number of data points or sequences, e.g.: len(X)
    p = number of parameters (free parameters)
    plogN = increase when increasing model complexity (penalty)

    ## Brief explanation

    ### Free parameters
    - transition matrix is n*n, sum of all probabilities is 1, then n(n-1) free params exists
    - starting probabilities, n, sum of all probabilities is 1, then n - 1 free params exists
    - gaussian free paramters, variances and means, the covmat diagonal is the variance, and
      with the mean represents the free paramters, per each state and feature
    Would be: (n-1) + n*(n-1) + n*d + n*2, giving -> n^2-1 2*(n*d) where n is states and d features
               initp  transmat  means variance

    ## Documentation and references:
     - https://en.wikipedia.org/wiki/Hidden_Markov_model#Architecture
     - http://hmmlearn.readthedocs.io/en/stable/api.html#hmmlearn.hmm.GaussianHMM
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection based on BIC scores
        
        bics_model = []

        for n in range(self.min_n_components, self.max_n_components + 1):
            try:
                model = self.base_model(n)
                logL = model.score(self.X, self.lengths)
                logN = math.log(len(self.X))
                # free parameters
                d = self.X.shape[1]
                p = math.pow(n,2) - 1 + 2*n*d
                # bayesian information cr#iterions
                bic = -2 * logL + p * logN
                bics_model.append((bic, model))
            except:
                pass # print("Unexpected error:", sys.exc_info()[0])

        if len(bics_model):
            return min(bics_model)[1]
        else:
            return None

class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))

    ## Bried Explanation
     - Higher score is better, DIC doesn't focus on complexity
     - log(P(X(i)) is the log likelihood return by the model.score
     - log(P(X(all but i) is the model score when evaluating the model on all words
       other than the word for which we're training this particular model
     - 1/(M-1) is the len of other words 
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection based on DIC scores

        # all but this_word
        other_words = [self.hwords[word] for word in self.words if word != self.this_word]

        score, model = float('-Inf'), None

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            try:
                state_model = self.base_model(num_states)
                this = state_model.score(self.X, self.lengths)
                others = sum([state_model.score(x,length) for x,length in other_words])/len(other_words)
                dic = this - others
                if dic > score:
                    score, model = dic, state_model
            except:
                pass

        return model

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def get_score(self, training, test, num_states):
        """
        Create a gaussian model and do the fit with the training data and get the score
        with the test data
        """
        model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000, 
                            random_state=self.random_state, verbose=False).fit(training[0], training[1])
        return model.score(test[0], test[1])

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # TODO implement model selection based on CV scores
        
        score, states, n_splits = float('-Inf'), -1, min(len(self.sequences),3)
        
        if n_splits == 0: return None

        split_method = None if n_splits == 1 else KFold(n_splits=n_splits)

        for num_states in range(self.min_n_components, self.max_n_components + 1):
            scores = []

            try:
                if n_splits == 1:
                    training = (self.X, self.lengths)
                    test = (self.X, self.lengths)
                    scores.append(self.get_score(training, test, num_states))
                else:
                    for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                        # get the splits
                        training = combine_sequences(cv_train_idx, self.sequences)
                        test = combine_sequences(cv_test_idx, self.sequences)
                        scores.append(self.get_score(training, test, num_states))  
            except:
                pass # print("Unexpected error:", num_states, sys.exc_info())
                    
            # bookeeping
            if len(scores):
                avg_score = sum(scores)/len(scores)
                if avg_score >= score: 
                    score, states = avg_score, num_states

        if states >= self.min_n_components:
            return GaussianHMM(n_components=states, covariance_type="diag", n_iter=1000, 
                                random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
        else:
            return None