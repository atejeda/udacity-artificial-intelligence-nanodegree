import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = []
    y = []

    # sliding windows or pairs
    steps = len(series) - window_size
    
    for i in range(steps):
        X.append(series[i : i + window_size])
        y.append(series[i + window_size])
            
    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y

# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size):
    model = Sequential()
    model.add(LSTM(5, input_shape = (window_size, 1), activation = 'tanh'))
    model.add(Dense(1))
    return model


### TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    # http://www.asciitable.com/ [97 122]
    p = ['!', ',', '.', ':', ';', '?'] # punctuation
    t = [c if (96 < ord(c) and ord(c) < 123) or (c in p) else ' ' for c in text]
    return ''.join(t)

### TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = []
    outputs = []
 
    steps = int(np.ceil((len(text) - window_size)/step_size))
    
    # sliding windows or pairs
    for i in range(steps):
        l = i * step_size
        r = i * step_size + window_size
        inputs.append(text[l:r])
        outputs.append(text[r])

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    model = Sequential()
    model.add(LSTM(200, input_shape = (window_size, num_chars), activation = 'tanh'))
    model.add(Dense(num_chars, activation = 'softmax'))
    return model
