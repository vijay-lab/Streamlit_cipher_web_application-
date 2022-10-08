import streamlit as st
import pandas as pd
import pickle
import sklearn

import pandas as pd
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.metrics import f1_score,precision_score,recall_score
import pickle

st.title("Encrypted Text Decryption App")
cipher_text = st.text_input("Enter encrypted text", "")


loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
test_vec = loaded_vectorizer.transform([cipher_text])
cipher_class = loaded_model.predict(test_vec)

st.write(cipher_class)
