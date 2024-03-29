# -*- coding: utf-8 -*-
"""xlnet_model1

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1As7xOsH_Udj4id9f64-Lme3Fuo9Y7PaO
"""

# !pip
# install - U
# tensorflow
# tensorflow_datasets
# tensorflow_text
# zhon
# sentencepiece
# transformers
# focal - loss
# tfa - nightly
# !git
# clone
# https: // github.com / cardiffnlp / tweeteval.git
# !pip
# install
# wordsegment
# !pip
# install
# textblob

# Commented out IPython magic to ensure Python compatibility.
# Importing required libraries
import pandas as pd
import nltk
# For regular expressions
import re

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')

from nltk.corpus import stopwords
import os, pathlib, re, nltk, pickle, string
from textblob import TextBlob
import nltk
from nltk.corpus import words, brown
import seaborn as sns
import spacy
import keras
# from keras.layers.core import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from zhon import hanzi
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve
import csv
from tqdm.notebook import tqdm
from nltk.tokenize import word_tokenize
# from focal_loss import BinaryFocalLoss
# Importing wordcloud for plotting word clouds and textwrap for wrapping longer text
from wordcloud import WordCloud
from textwrap import wrap
from collections import Counter
# import tensorflow as tf
# import tensorflow_text as text
# from tensorflow.keras import Input, layers, losses, preprocessing, utils
# from tensorflow.keras.callbacks import ModelCheckpoint
# from tensorflow.keras.models import Model
# from tensorflow.keras.optimizers import Adam
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from nltk.stem import PorterStemmer
# import tensorflow_addons as tfa
import itertools
from sklearn.metrics import f1_score

try:
    print("gdfg")
    #%tensorflow_version 2.x

except Exception:
    pass

base_dir = '/content/tweeteval/datasets/'
hate_dir = base_dir + "hate"
offensive_dir = base_dir + "offensive"
sentiment_dir = base_dir + "sentiment"

# Dictionary of English Contractions
contractions_dict = {"ain't": "are not", "'s": " is", "aren't": "are not",
                     "can't": "cannot", "can't've": "cannot have",
                     "'cause": "because", "could've": "could have", "couldn't": "could not",
                     "couldn't've": "could not have", "didn't": "did not", "doesn't": "does not",
                     "don't": "do not", "hadn't": "had not", "hadn't've": "had not have",
                     "hasn't": "has not", "haven't": "have not", "he'd": "he would",
                     "he'd've": "he would have", "he'll": "he will", "he'll've": "he will have",
                     "how'd": "how did", "how'd'y": "how do you", "how'll": "how will",
                     "I'd": "I would", "I'd've": "I would have", "I'll": "I will",
                     "I'll've": "I will have", "I'm": "I am", "I've": "I have", "isn't": "is not",
                     "it'd": "it would", "it'd've": "it would have", "it'll": "it will",
                     "it'll've": "it will have", "let's": "let us", "ma'am": "madam",
                     "mayn't": "may not", "might've": "might have", "mightn't": "might not",
                     "mightn't've": "might not have", "must've": "must have", "mustn't": "must not",
                     "mustn't've": "must not have", "needn't": "need not",
                     "needn't've": "need not have", "o'clock": "of the clock", "oughtn't": "ought not",
                     "oughtn't've": "ought not have", "shan't": "shall not", "sha'n't": "shall not",
                     "shan't've": "shall not have", "she'd": "she would", "she'd've": "she would have",
                     "she'll": "she will", "she'll've": "she will have", "should've": "should have",
                     "shouldn't": "should not", "shouldn't've": "should not have", "so've": "so have",
                     "that'd": "that would", "that'd've": "that would have", "there'd": "there would",
                     "there'd've": "there would have", "they'd": "they would",
                     "they'd've": "they would have", "they'll": "they will",
                     "they'll've": "they will have", "they're": "they are", "they've": "they have",
                     "to've": "to have", "wasn't": "was not", "we'd": "we would",
                     "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have",
                     "we're": "we are", "we've": "we have", "weren't": "were not", "what'll": "what will",
                     "what'll've": "what will have", "what're": "what are", "what've": "what have",
                     "when've": "when have", "where'd": "where did", "where've": "where have",
                     "who'll": "who will", "who'll've": "who will have", "who've": "who have",
                     "why've": "why have", "will've": "will have", "won't": "will not",
                     "won't've": "will not have", "would've": "would have", "wouldn't": "would not",
                     "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
                     "y'all'd've": "you all would have", "y'all're": "you all are",
                     "y'all've": "you all have", "you'd": "you would", "you'd've": "you would have",
                     "you'll": "you will", "you'll've": "you will have", "you're": "you are",
                     "you've": "you have"}

# Regular expression for finding contractions
contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))


# Function for expanding contractions
def expand_contractions(text, contractions_dict=contractions_dict):
    def replace(match):
        return contractions_dict[match.group(0)]

    return contractions_re.sub(replace, text)


# Removing all punctuation
def identify_tokens(row):
    tweets = row['tweets']
    tokens = nltk.word_tokenize(tweets)
    # taken only words (not punctuation)
    token_words = [w for w in tokens if w.isalpha()]
    return token_words


stemming = PorterStemmer()


def stem_list(row):
    my_list = row['words']
    stemmed_list = [stemming.stem(word) for word in my_list]
    return (stemmed_list)


stops = set(stopwords.words("english"))


def remove_stops(row):
    my_list = row['words']
    meaningful_words = [w for w in my_list if not w in stops]
    return (meaningful_words)


def rejoin_words(row):
    my_list = row['stem_meaningful']
    joined_words = (" ".join(my_list))
    return joined_words


from wordsegment import load, segment


def segmentTweets(row):
    load()
    # tweets = row['tweets']
    segment(row)
    return segment


def preprocess_tweet(tweet):
    tweet = tweet.translate(str.maketrans('', '', string.punctuation))
    # tweet = tweet.replace('@user', '')
    tweet = tweet.apply(lambda x: expand_contractions(x))
    tweet = tweet.lower()
    tweet = tweet.apply(identify_tokens, axis=1)
    tweet = tweet.apply(stem_list, axis=1)
    tweet = tweet.apply(remove_stops, axis=1)
    tweet = tweet.apply(rejoin_words, axis=1)
    return tweet


def readfile(text):
    pd_list = []
    with open(text, 'r') as f:
        for tweet in f.read().splitlines():
            tweet = preprocess_tweet(tweet)
            pd_list.append(tweet)
    return pd_list


def readfile_label(text):
    pd_list = []
    with open(text, 'r') as f:
        for tweet in f.read().splitlines():
            pd_list.append(int(tweet))
    return pd_list


# Pre-process csv and merge into a Dataframe
# Hate DataFrame Data
import os
hate_dict_train = {'text': readfile(os.path.join(hate_dir, "train_text.txt")),
                   'label': readfile_label(os.path.join(hate_dir, "train_labels.txt"))}
hate_dict_val = {'text': readfile(os.path.join(hate_dir, "val_text.txt")),
                 'label': readfile_label(os.path.join(hate_dir, "val_labels.txt"))}
hate_dict_test = {'text': readfile(os.path.join(hate_dir, "test_text.txt")),
                  'label': readfile_label(os.path.join(hate_dir, "test_labels.txt"))}
hate_val_df = pd.DataFrame(hate_dict_val)
hate_test_df = pd.DataFrame(hate_dict_test)
hate_frames = [hate_train_df, hate_val_df, hate_test_df]
df_hate = pd.concat(hate_frames)
not_hate = df_hate[df_hate['label'] == 0]
hate = df_hate[df_hate['label'] == 1]

# sentiment DataFrame
sentiment_dict_train = {'text': readfile(os.path.join(sentiment_dir, "train_text.txt")),
                        'label': readfile_label(os.path.join(sentiment_dir, "train_labels.txt"))}
sentiment_dict_val = {'text': readfile(os.path.join(sentiment_dir, "val_text.txt")),
                      'label': readfile_label(os.path.join(sentiment_dir, "val_labels.txt"))}
sentiment_dict_test = {'text': readfile(os.path.join(sentiment_dir, "test_text.txt")),
                       'label': readfile_label(os.path.join(sentiment_dir, "test_labels.txt"))}
sentiment_train_df = imbalance_under_sampling(pd.DataFrame(sentiment_dict_train))
sentiment_val_df = pd.DataFrame(sentiment_dict_val)
sentiment_test_df = pd.DataFrame(sentiment_dict_test)
sentiment_frames = [sentiment_train_df, sentiment_val_df, sentiment_test_df]
df_sentiment = pd.concat(sentiment_frames)
not_sentiment = df_sentiment[df_sentiment['label'] == 0]
sentiment = df_sentiment[df_sentiment['label'] == 1]

# Offensive DataFrame
offensive_dict_train = {'text': readfile(os.path.join(offensive_dir, "train_text.txt")),
                        'label': readfile_label(os.path.join(offensive_dir, "train_labels.txt"))}
offensive_dict_val = {'text': readfile(os.path.join(offensive_dir, "val_text.txt")),
                      'label': readfile_label(os.path.join(offensive_dir, "val_labels.txt"))}
offensive_dict_test = {'text': readfile(os.path.join(offensive_dir, "test_text.txt")),
                       'label': readfile_label(os.path.join(offensive_dir, "test_labels.txt"))}
offensive_train_df = imbalance_under_sampling(pd.DataFrame(offensive_dict_train))
offensive_val_df = pd.DataFrame(offensive_dict_val)
offensive_test_df = pd.DataFrame(offensive_dict_test)
offensive_frames = [offensive_train_df, offensive_val_df, offensive_test_df]
df_offensive = pd.concat(offensive_frames)
not_offensive = df_offensive[df_offensive['label'] == 0]
offensive = df_offensive[df_offensive['label'] == 1]

hate = df_hate[df_hate['label'] == 1]
hate

from transformers import TFXLNetModel, XLNetTokenizer

# xlnet-large-cased
xlnet_tokenizer = XLNetTokenizer.from_pretrained('xlnet-base-cased')
xlnet_model = TFXLNetModel.from_pretrained('xlnet-base-cased')


def create_xlnet(xl_model):
    """ Creates the model. It is composed of the XLNet main block and then
    a classification head its added
    """
    # Define token ids as inputs
    word_ids = tf.keras.Input(shape=(120,), name='word_ids', dtype='int32')
    word_attention = tf.keras.Input(shape=(120,), name='word_attention', dtype='int32')
    # word_seq = tf.keras.Input(shape=(120,), name='word_seq', dtype='int32')

    # Call XLNet model
    xlnet_encodings = xl_model([word_ids, word_attention])[0]

    # CLASSIFICATION HEAD
    # Collect last step from last hidden state (CLS)
    doc_encoding = tf.squeeze(xlnet_encodings[:, -1:, :], axis=1)
    # Apply dropout for regularization
    dense = tf.keras.layers.Dense(32, activation='relu', name='encoding')(doc_encoding)
    drop = tf.keras.layers.Dropout(0.1)(dense)
    # Final output
    outputs = tf.keras.layers.Dense(1, activation='sigmoid', name='outputs')(drop)

    # Compile model
    model = tf.keras.Model(inputs=[word_ids, word_attention], outputs=[outputs])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=2e-5), loss=BinaryFocalLoss(gamma=2),
                  metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall()])

    return model


def get_inputs(tweets, tokenizer, max_len=120):
    """ Gets tensors from text using the tokenizer provided"""
    inps = [tokenizer.encode_plus(t, max_length=max_len, pad_to_max_length=True, add_special_tokens=True) for t in
            tweets]
    inp_tok = np.array([a['input_ids'] for a in inps])
    ids = np.array([a['attention_mask'] for a in inps])
    return inp_tok, ids


def plot_metrics(pred, true_labels):
    """Plots a ROC curve with the accuracy and the AUC"""
    acc = accuracy_score(true_labels, np.array(pred.flatten() >= .5, dtype='int'))
    fpr, tpr, thresholds = roc_curve(true_labels, pred)
    auc = roc_auc_score(true_labels, pred)

    fig, ax = plt.subplots(1, figsize=(8, 8))
    ax.plot(fpr, tpr, color='red')
    ax.plot([0, 1], [0, 1], color='black', linestyle='--')
    ax.set_title(f"AUC: {auc}\nACC: {acc}");
    return fig


callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5, min_delta=0.001, restore_best_weights=True),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_accuracy', factor=1e-6, patience=2, verbose=0, mode='auto',
                                         min_delta=0.001, cooldown=0, min_lr=1e-6)
]


def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=None, normalize=True):
    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45)
        plt.yticks(tick_marks, target_names)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
    plt.show()


hate_train_input = get_inputs(hate_train_df['text'], xlnet_tokenizer)
hate_val_input = get_inputs(hate_val_df['text'], xlnet_tokenizer)
hate_test_input = get_inputs(hate_test_df['text'], xlnet_tokenizer)

xlnet_hate = create_xlnet(xlnet_model)
xlnet_hate.summary()
hist = xlnet_hate.fit(x=hate_train_input, y=hate_train_df['label'], epochs=1, batch_size=16,
                      validation_data=(hate_val_input, hate_val_df['label']), callbacks=callbacks)

preds = xlnet_hate.predict(hate_test_input, verbose=True)
y_pred = [i[0] for i in preds.round().astype(int)]
cm = confusion_matrix(hate_test_df['label'], y_pred)
plot_confusion_matrix(cm, normalize=False, target_names=['Not_Hate', 'hate'], title="Confusion Matrix for hate")

f1_score(hate_test_df.label, y_pred, average='macro')

##########################################################
#########################################################
# This has worked for a colleague of mine, when he completed his pre processing, so the model part I know works