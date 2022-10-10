import streamlit as st
import pandas as pd
import pickle
import sklearn
import random
from sklearn.feature_extraction.text import TfidfVectorizer


# Preemptying Strealit default footer
footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with <span style = "color:red">❤</span> by <a ' href="https://www.linkedin.com/in/tapanvijay/" target="_blank"><span style = "color:white">Tapan Vijayvergiya</span></a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)



st.title("Encrypted Text Decryption App")
plain_text_df = pd.read_csv('test.csv')


def random_index(plain_text_df):
    return random.randint(0,len(plain_text_df))

random_cipher_df_index = random_index(plain_text_df)

if st.button('Generate a new sample Cipher Text'):
  random_cipher_df_index = random_index(plain_text_df)


st.dataframe(plain_text_df.iloc[random_cipher_df_index])

st.write("Use this cipher text to test the application")
st.text(plain_text_df.ciphertext[random_cipher_df_index])

cipher_text = st.text_area( label = "Enter Encrypted Text to Decrypt")
            

def predict_cipher_class(cipher_text):
    
    loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    plain_text_dict = pickle.load(open('plain_text_dict.var', 'rb'))
    test_vec = loaded_vectorizer.transform([cipher_text])
    cipher_label = loaded_model.predict(test_vec)
    
    return cipher_label,plain_text_dict


cipher_class,plain_text_dict = predict_cipher_class(cipher_text)


def decryption_block_l1(ct):
    alphabet = 'abcdefghijklmnopqrstuvwxy'
    key = [15, 24, 11, 4]
    key_index = 0
    text = ''

    for char in ct:
        char_pos_alpha = alphabet.find(char)
        if char_pos_alpha != -1:
            char_pos_alpha = (char_pos_alpha - key[key_index]) % 25
            plain_char_decry = alphabet[char_pos_alpha]
            key_index = (key_index + 1) % 4


        elif (char_pos_alpha := alphabet.upper().find(char)) != -1:
            char_pos_alpha = (char_pos_alpha - key[key_index]) % 25
            plain_char_decry = alphabet[char_pos_alpha].upper()
            key_index = (key_index + 1) % 4

        else:
            plain_char_decry = char

        text += plain_char_decry

    return text


from itertools import cycle, chain

def fence_pattern(text_len,rail = 21):
    rail_pattern = cycle(chain(range(rail), range(rail - 2, 0, -1)))
    return zip(rail_pattern, range(text_len))


def decryption_block_l2(ct):
    fence = fence_pattern(len(ct))
    fence_msg = zip(ct, sorted(fence))
    return "".join(char for char, _ in sorted(fence_msg, key = lambda item: item[1][1]))





from urllib.request import urlopen

# Downloading the key file and storing it as key_level3 in memory
with urlopen("https://www.gutenberg.org/files/46464/46464-0.txt") as key_file:
    key_level3 = key_file.read().decode('utf-8').replace('\r', ' ').replace('\n', ' ')


def decryption_block_l3(text, key=key_level3):
    x = ''.join([key_level3[int(n)] for n in text.split(' ') if n !=''])
    return x

def find_pt_index(decrypted_text):
    decrypted_text_without_padding = ""


    for pad in range(100):
        start = pad // 2
        end = len(decrypted_text) - (pad + 1) // 2

        try:
            if plain_text_dict[decrypted_text[start:end]]  > 0:
                decrypted_text_without_padding = decrypted_text[start:end]
            break

        except KeyError:
            continue

    return decrypted_text_without_padding



key4 = [49, 36, 97, 134, 109, 43, 4, 250, 67, 119, 137, 145, 139, 96, 180, 34, 149, 124, 252, 17, 90, 66, 119, 90, 189, 154, 228, 249, 189, 132, 133, 80, 144, 129, 8, 48, 162, 33, 208, 124, 176, 51, 51, 253, 201, 19, 40, 34, 108, 245, 150, 222, 205, 226, 82, 239, 75, 167, 42, 244, 128, 62, 13, 178, 60, 74, 82, 62, 127, 94, 32, 29, 251, 196, 250, 139, 62, 149, 235, 20, 76, 40, 143, 191, 184, 20, 104, 72, 128, 117, 178, 119, 138, 203, 77, 104, 244, 100, 24, 47, 49, 179, 62, 255, 70, 92, 163, 181, 215, 248, 123, 236, 239, 43, 49, 190, 157, 76, 53, 116, 188, 144, 75, 203, 146, 184, 159, 182, 49, 253, 14, 70, 202, 95, 162, 119, 113, 239, 181, 143, 3, 208, 163, 17, 74, 67, 159, 250, 249, 110, 255, 46, 83, 110, 16, 250, 166, 207, 157, 191, 18, 118, 250, 8, 143, 53, 98, 40, 17, 27, 161, 6, 147, 80, 223, 75, 61, 150, 187, 155, 86, 227, 255, 32, 188, 180, 137, 219, 215, 135, 247, 247, 200, 252, 82, 100, 126, 24, 179, 71, 0, 67, 19, 27, 26, 155, 197, 183, 213, 76, 246, 200, 244, 4, 75, 212, 70, 131, 154, 89, 169, 251, 16, 113, 73, 62, 19, 170, 190, 202, 155, 27, 28, 23, 78, 85, 153, 19, 146, 170, 107, 225, 175, 30, 173, 74, 95, 244, 187, 178, 121, 54, 137, 162, 10, 151, 155, 63, 3, 139, 232, 13, 184, 219, 180, 119, 175, 112, 211, 156, 62, 76, 85, 241, 52, 138, 142, 156, 157, 14, 161, 235, 103, 101, 252, 66, 153, 156, 234, 75, 43, 21, 105, 111, 106, 240, 175, 214, 108, 177, 202, 9, 212, 29, 164, 200, 60, 242, 13, 115, 121, 201, 58, 82, 113, 174, 118, 152, 241, 3, 151, 238, 135, 220, 209, 2, 94, 228, 237, 116, 58, 6, 21, 27, 236, 227, 198, 233, 190, 69, 254, 205, 63, 239, 20, 122, 111, 235, 126, 165, 168, 150, 166, 12, 125, 161, 188, 22, 8, 46, 229, 75, 54, 186, 213, 99, 42, 47, 26, 96, 153, 90, 123, 26, 223, 3, 151, 229, 203, 16, 98, 9, 116, 186, 188, 96, 102, 77, 53, 239, 208, 228, 121, 200, 217, 18, 12, 172, 212, 233, 27, 39, 248, 211, 44, 180, 163, 46, 175, 180, 26, 182, 207, 215, 141, 15, 244, 227, 219, 6, 12, 181, 58, 79, 155, 17, 73, 171, 215, 78, 1, 177, 115, 236, 68, 21, 194, 172, 84, 177, 224, 234, 7, 40, 232, 214, 240, 66, 59, 79, 153, 4, 190, 216, 221, 47, 156, 23, 111, 118, 137, 254, 140, 130, 228, 221, 68, 25, 13, 86, 118, 20, 190, 74, 145, 183, 62, 195, 223, 182, 145, 86, 107, 151, 198, 215, 254, 74, 204, 113, 120, 195, 187, 198, 245, 46, 203, 119, 217, 6, 2, 226, 188, 10, 87, 84, 109, 43, 226, 79, 103, 28, 72, 145, 170, 70, 246, 160, 186, 121, 72, 247, 158, 88, 34, 140, 72, 81, 38, 250, 35, 92, 181, 163, 120, 63, 16, 51, 179, 150, 212, 159, 255, 122, 225, 114, 24, 73, 196, 80, 253, 5, 165, 241, 60, 236, 176, 68, 251, 158, 14, 90, 181, 134, 174, 232, 87, 114, 10, 32, 15, 213, 128, 227, 83, 28, 43, 75, 218, 234, 216, 53, 200, 51, 44, 118, 232, 78, 73, 106, 82, 48, 138, 230, 86, 252, 114, 3, 227, 17, 68, 61, 101, 4, 208, 79, 103, 97, 29, 191, 29, 151, 145, 45, 95, 202, 199, 70, 169, 150, 201, 255, 58, 112, 104, 66, 181, 118, 61, 49, 164, 200, 32, 79, 27, 131, 161, 217, 219, 55, 23, 39, 248, 155, 197, 41, 40, 116, 229, 106, 131, 220, 137, 23, 202, 106, 100, 23, 14, 72, 238, 157, 200, 38, 235, 26, 141, 157, 166, 14, 225, 13, 195, 61, 163, 86, 134, 247, 33, 100, 169, 170, 71, 114, 231, 14, 192, 155, 122, 218, 86, 83, 237, 71, 113, 176, 75, 217, 133, 91, 214, 24, 134, 168, 40, 27, 218, 11, 59, 87, 192, 56, 58, 27, 241, 214, 107, 235, 157, 197, 69, 126, 91, 67, 185, 37, 96, 46, 205, 17, 226, 227, 127, 178, 45, 197, 117, 151, 128, 82, 35, 98, 112, 45, 157, 233, 79, 180, 147, 74, 195, 255, 193, 96, 201, 12, 88, 234, 253, 174, 0, 15, 28, 96, 231, 100, 70, 29, 200, 111, 110, 55, 85, 205, 130, 222, 251, 154, 44, 107, 170, 224, 86, 40, 156, 208, 185, 39, 48, 167, 243, 248, 17, 227, 70, 120, 141, 83, 245, 92, 76, 142, 245, 97, 165, 177, 154, 147, 175, 222, 166, 177, 222, 73, 174, 234, 26, 167, 194, 130, 210, 239, 198, 70, 85, 253, 3, 21, 131, 93, 108, 92, 158, 137, 186, 9, 110, 120, 124, 248, 20, 102, 239, 167, 181, 12, 165, 229, 32, 131, 23, 57, 194, 182, 194, 181, 65, 3, 177, 2, 129, 157, 211, 84, 64, 190, 144, 122, 162, 198, 103, 144, 117, 182, 157, 205, 231, 165, 253, 120, 205, 117, 18, 139, 238, 244, 172, 4, 209, 140, 199, 15, 6, 217, 5, 213, 117, 209, 58, 104, 150, 7, 248, 106, 29, 245, 224, 224, 95, 243, 79, 225, 163, 179, 60, 108, 144, 95, 191, 109, 24, 18, 10, 87, 233, 8, 179, 195, 106, 125, 13, 35, 53, 202, 25, 28, 208, 18, 19, 17, 189, 254, 44, 29, 11, 197, 98, 59, 188, 74, 44, 221, 161, 108, 4, 160, 19, 128, 198, 37, 119, 17, 40, 22, 236, 214, 76, 108, 125, 49, 16, 136, 38, 234, 164, 142, 40, 120, 11, 73, 42, 54, 181, 62, 230, 7, 101, 113, 163, 172, 225, 86, 88, 17, 40, 40, 236, 121, 104, 50, 49, 243, 54, 231, 185, 238, 121, 52, 78, 192, 31, 61, 234, 153, 120, 177, 143, 233, 31, 150, 20, 172, 70, 224, 141, 100, 69, 9, 38, 66, 241, 102, 175, 222, 51, 251, 230, 127, 220, 36, 116, 226, 174, 94, 101, 202, 46, 126, 87, 131, 111, 123, 110, 242, 61, 120, 238, 241, 246, 161, 24, 209, 99, 144, 73, 152, 143, 70, 180, 143, 20, 118, 168, 63, 174, 142, 209, 165, 92, 108, 83, 88, 61, 149, 157, 247, 240, 230, 83, 198, 167, 247, 199, 102, 83, 230, 66, 217, 158, 194, 219, 226, 226, 95, 110, 56, 161, 154, 114, 46, 94, 191, 115, 60, 247, 205, 113, 167, 21, 251, 135, 72, 29, 3, 26, 161, 2, 48, 106, 228, 71, 184, 198, 171, 244, 108, 134, 70, 153, 144, 113, 29, 178, 113, 160, 173, 208, 8, 103, 48, 114, 244, 77, 126, 188, 159, 161, 163, 41, 251, 199, 245, 157, 84, 184, 251, 189, 91, 177, 159, 187, 147, 245, 88, 121, 52, 61, 29, 22, 94, 179, 127, 241, 255, 191, 90, 222, 29, 154, 153, 253, 27, 254, 95, 118, 31, 159, 52, 62, 221]


import base64
def decryption_block_l4(text, key=key4):
    return ''.join([chr(a^b) for a,b in zip(base64.b64decode(text),key)])


def decrypted_text_switch(cipher_text,cipher_class):
    dec_text = ""
    if cipher_class == 1:
        dec_text = find_pt_index(decryption_block_l1(cipher_text))

    if cipher_class == 2:
        dec_text = find_pt_index(decryption_block_l1(decryption_block_l2(cipher_text)))

    if cipher_class == 3:
        dec_text = find_pt_index(decryption_block_l1(decryption_block_l2(decryption_block_l3(cipher_text))))

    if cipher_class == 4:
        dec_text = find_pt_index(decryption_block_l1(decryption_block_l2(decryption_block_l3(decryption_block_l4(cipher_text)))))
    
    return dec_text

dec_text = decrypted_text_switch(cipher_text,cipher_class)



if len(cipher_text) > 0:
  
  st.write("The Encryption level is :", str(cipher_class),"and the decrypted text is \" ",dec_text,"\"")
