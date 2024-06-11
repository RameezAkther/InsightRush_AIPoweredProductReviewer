import pandas as pd
import numpy as np
import torch
import re
import string
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from keras.preprocessing.sequence import pad_sequences
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

import os

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Global variables for positive and negative counts
pos1 = 0
neg1 = 0

# Function to get the maximum numbered CSV file in a directory
def get_max_numbered_csv(directory):
    files = os.listdir(directory)
    max_number = float('-inf')
    max_filename = None
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

# Function to preprocess text
def clean_text(text):
    text = re.sub(r'[^A-Za-zÀ-ú ]+', '', text)
    text = re.sub('book|one', '', text)
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to preprocess data
def preprocess_data(df):
    df['Rating'] = df['Rating'].astype(str)
    df['Rating'] = df['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
    df['Label'] = df['Rating'].apply(lambda x: 1 if x >= 3 else 0)
    df['Combined'] = df['Review Title'].apply(str) + ' ' + df['Review Body']
    df['Combined'] = df['Combined'].apply(clean_text)
    return df

# Function to predict and evaluate sentiment using BERT model
def predict_and_evaluate(data):
    global pos1, neg1
    
    # Load BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("Dmyadav2001/Sentimental-Analysis")
    model = AutoModelForSequenceClassification.from_pretrained("Dmyadav2001/Sentimental-Analysis")
    
    # Initialize sentiment analysis pipeline
    sentiment_analysis = pipeline("text-classification", model=model, tokenizer=tokenizer)
    
    # Convert Pandas Series to list
    combined_texts = data['Combined'].tolist()
    
    # Predict sentiment and count positive/negative labels
    predictions = sentiment_analysis(combined_texts)
    print(predictions)
    
    # Threshold for positive sentiment
    threshold = 0.9  # You can adjust this threshold as needed
    
    # Count positive/negative labels based on threshold
    pos1 = sum(1 for pred in predictions if  pred['label'] == 'LABEL_1')
    neg11 = sum(1 for pred in predictions if pred['label'] == 'LABEL_0')
    neg12 = sum(1 for pred in predictions if pred['label'] == 'LABEL_2')
    neg1=neg11+neg12

# Function to perform classification
def perform_classification():
    dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data"
    file = get_max_numbered_csv(dir)
    dir = os.path.join(dir, file)
    df = pd.read_csv(dir)
    df = preprocess_data(df)
    df.to_csv("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data\\" + file, index=False)
    predict_and_evaluate(df)

# Perform classification and print results
perform_classification()
print("Positive Count:", pos1)
print("Negative Count:", neg1)