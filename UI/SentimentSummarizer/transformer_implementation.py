import pandas as pd
import numpy as np
import re
import string
import nltk
import os
import sys
import warnings
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf

warnings.filterwarnings('ignore')

def normalize_text(text):
    stemmer = SnowballStemmer("english")
    normalized_text = []
    for word in text.split():
        stemmed_word = stemmer.stem(word)
        normalized_text.append(stemmed_word)
    return ' '.join(normalized_text)

def remove_stopwords(texto):
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(texto.lower())
    return " ".join([token for token in tokens if token not in stop_words])

def clean_text(text):
    text = re.sub(r'[^A-Za-zÀ-ú ]+', '', text)
    text = re.sub('book|one', '', text)
    text = text.lower()

    text = text.translate(str.maketrans('', '', string.punctuation))

    text = re.sub(r'\s+', ' ', text).strip()
    return text

def rameez(z, kind):
    if kind == "amazon":
        z['rating_value'] = z['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        z['label'] = z['rating_value'].apply(lambda x: 1 if x >= 3 else 0)
        z.drop(columns=["Unnamed: 0","Rating","rating_value",'productTitle'], inplace=True)
        z.columns = ['title', 'text','label_on_rating']
        z['text'] = z['text'].apply(str) + ' ' + z['title'].apply(str)
        z.drop('title', axis = 1, inplace = True)
        return z
    elif kind == "flipkart":
        z['rating_value'] = z['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        z['label'] = z['rating_value'].apply(lambda x: 1 if x >= 3 else 0)
        z.drop(columns=["Rating","rating_value"], inplace=True)
        z.columns = ['title', 'text','label_on_rating']
        z['text'] = z['text'].apply(str) + ' ' + z['title'].apply(str)
        z.drop('title', axis = 1, inplace = True)
        return z

def get_max_numbered_file(directory):
    # Get list of files in the directory
    files = os.listdir(directory)
    
    # Initialize variables to keep track of max number and corresponding filename
    max_number = float('-inf')
    max_filename = None
    
    # Iterate through files to find the max numbered file
    for file_name in files:
        if file_name.endswith('.csv'):
            try:
                file_number = int(os.path.splitext(file_name)[0])
                if file_number > max_number:
                    max_number = file_number
                    max_filename = file_name
            except ValueError:
                continue
    
    return max_filename 

def clean2(a):
    a['text'] = a['text'].apply(clean_text)
    a['text'] = a['text'].apply(remove_stopwords)
    a['text'] = a['text'].apply(normalize_text) 
    return a

def predict_and_evaluate(data):
    # Load tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    
    # Tokenize and encode each text in the data
    encoded_texts = [tokenizer.encode_plus(text, max_length=100, padding='max_length', truncation=True, return_tensors='tf') for text in data['text']]
    
    # Extract input IDs from the encoded texts and remove the extra dimension
    sequences_padded = np.array([encoded_text['input_ids'].numpy().squeeze() for encoded_text in encoded_texts])
    
    # Load the trained model
    model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')
    
    # Make predictions on the padded sequences
    outputs = model.predict(sequences_padded)
    predictions = tf.nn.softmax(outputs.logits, axis=-1).numpy()
    print(predictions)
    # Determine the predicted labels
    predicted_labels = ['positive' if prediction[1] >= 0.5 else 'negative' for prediction in predictions]
    #data['predicted_labels']=predicted_labels
    # Evaluate the model's performance
    positive_count = sum(1 for label in predicted_labels if label == "positive")
    negative_count = sum(1 for label in predicted_labels if label == "negative")
    print("The Model's Predicted Positive count:", positive_count)
    print("The Model's Predicted Negative count:", negative_count)
    
    correct_count = 0
    wrong_count = 0
    for org_label, pred_label in zip(data['label_on_rating'], predicted_labels):
        if (org_label == 1 and pred_label == 'positive') or (org_label == 0 and pred_label == 'negative'):
            correct_count += 1
        else:
            wrong_count += 1
    
    accuracy = correct_count / len(data)
    print("Accuracy:", accuracy)
    
    return data

dir = "C:\\Users\\praga\\Desktop\\aiproject\\Scraped Data"
file = get_max_numbered_file(dir)
dir = dir + "\\" + file
df = pd.read_csv(dir)
tem = input("What data\n1.Amazon\n2.Flipkart\nEnter you option(1 or 2):")
if tem == "1" :
    a=rameez(df,"amazon")
    a=clean2(a)
    a=predict_and_evaluate(a)
    a.to_csv("C:\\Users\\praga\\Desktop\\aiproject\\Predicted_CSV\\Modified1030.csv",index=False)
elif tem == "2":
    a=rameez(df,"flipkart")
    a=clean2(a)
    a=predict_and_evaluate(a)
    a.to_csv("Modified.csv",index=False)
else:
    print("Invalid option!")
    sys.exit()