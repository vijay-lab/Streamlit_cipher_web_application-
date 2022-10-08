import streamlit as st
import pandas as pd
import pickle
import sklearn

st.title("Encrypted Text Decryption App")
cipher_text = st.text_input("Enter encrypted text", "")


loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
test_vec = loaded_vectorizer.transform([cipher_text])
cipher_class = loaded_model.predict(test_vec)

st.write(cipher_class)
