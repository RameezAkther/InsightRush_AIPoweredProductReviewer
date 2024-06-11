import pandas as pd
import numpy as np
import tensorflow as tf
import torch
import re
import string
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from keras.layers import LSTM
from keras.initializers import Orthogonal
import os
import sys
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import warnings
warnings.filterwarnings('ignore')

pos1 = 0
pos2 = 0
pos3 = 0

neg1 = 0
neg2 = 0
neg3 = 0

# Ensure NLTK stopwords are downloaded
#nltk.download('stopwords')
#nltk.download('punkt')

#TF_ENABLE_ONEDNN_OPTS=0

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
    try:
        text = re.sub(r'[^A-Za-zÀ-ú ]+', '', text)
        text = re.sub('book|one', '', text)
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except:
        return text

def rameez(z):
    try:
        z['Rating'] = z['Rating'].astype(str)
        z['Rating'] = z['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        z['Label'] = z['Rating'].apply(lambda x: 1 if x >= 3 else 0)
        z['Combined'] = z['Review Title'].apply(str) + ' ' + z['Review Body']
        return z
    except:
        z['Rating'] = z['Rating'].astype(str)
    
        # Extract numeric ratings from the 'Rating' column
        z['Rating'] = z['Rating'].str.extract(r'(\d+\.\d+)').astype(float)
        
        # Apply the label based on the extracted ratings
        z['Label'] = z['Rating'].apply(lambda x: 1 if x >= 3 else 0)
        
        # Combine 'Review Title' and 'Review Body' into a single column
        z['Combined'] = z['Review Title'].apply(str) + ' ' + z['Review Body']
    
        return z
    """
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
    """
   
def clean2(a):
    a['Combined'] = a['Combined'].apply(clean_text)
    a['Combined'] = a['Combined'].apply(remove_stopwords)
    a['Combined'] = a['Combined'].apply(normalize_text) 
    return a

def predict_and_evaluate(data, max_len=100):
    global pos1
    global neg1
    with open(r"C:\Users\ramee\Desktop\AI Lab\Project\UI\SentimentSummarizer\models\Tokenizer.h5", 'rb') as handle:
        tokenizer = pickle.load(handle)  
    
    tokenizer.fit_on_texts(data['Combined']) 
    sequences = tokenizer.texts_to_sequences(data['Combined']) 
    word_index = tokenizer.word_index 

    sequences_padded = pad_sequences(sequences, maxlen=max_len)

    model = load_model(r"C:\Users\ramee\Desktop\AI Lab\Project\UI\SentimentSummarizer\models\CNN.h5") 
    predictions = model.predict(sequences_padded)

    """model_name = "LYTinn/lstm-finetuning-sentiment-model-3000-samples"
    tokenizer2 = AutoTokenizer.from_pretrained(model_name)
    model2 = AutoModelForSequenceClassification.from_pretrained(model_name)
    sentiment_pipeline = pipeline("text-classification", model=model2, tokenizer=tokenizer2)"""

    """predictions2 = sentiment_pipeline(data['Combined'].tolist())
    predicted_labels2 = [pred['label'] for pred in predictions2]
    #print(predictions2)
    pos2 = predicted_labels2.count('positive')
    neg2 = predicted_labels2.count('negative')"""

    

    #model2 = load_model(r"C:\Users\ramee\Desktop\AI Lab\Project\UI\Sentiment Classifier and Summarizer\models\LSTM.h5", custom_objects=custom_objects) 
    #predictions2 = model2.predict(sequences_padded)

    def get_label(prediction):
        return 'positive' if prediction >= 0.5 else 'negative'

    predicted_labels = [get_label(prediction) for prediction in predictions]

    #predicted_labels2 = [get_label(prediction) for prediction in predictions2]

    data['predicted_label'] = predicted_labels
    #data['predicted_label2'] = predicted_labels2

    positive_count = sum(1 for label in predicted_labels if label == "positive")
    negative_count = sum(1 for label in predicted_labels if label == "negative")

    #positive_count2 = sum(1 for label in predicted_labels2 if label == "positive")
    #negative_count2 = sum(1 for label in predicted_labels2 if label == "negative")

    #print("The Model's Predicted Positive count: ",positive_count)
    #print("The Model's Predicted Negative count: ",negative_count)

    #correct_count = 0
    #wrong_count = 0

    #for org_label, pred_label in zip(data['label_on_rating'], data['predicted_label']):
    #    if (org_label == 1 and pred_label == 'positive') or (org_label == 0 and pred_label == 'negative'):
    #        correct_count += 1
    #    else:
    #        wrong_count += 1
            
    pos1 = positive_count
    neg1 = negative_count

"""def trans(data):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    print(data.columns)
    encoded_texts = [tokenizer.encode_plus(text, max_length=100, padding='max_length', truncation=True, return_tensors='tf') for text in data['Combined']]
    
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
    
    #accuracy = correct_count / len(data)
    #print("Accuracy:", accuracy)
    """

def trans2(data):
    global pos3
    global neg3
    global pos2
    global neg2    
    # Load BERT tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained("MarieAngeA13/Sentiment-Analysis-BERT")
    model = AutoModelForSequenceClassification.from_pretrained("MarieAngeA13/Sentiment-Analysis-BERT")

    tokenizer2 = AutoTokenizer.from_pretrained("Dmyadav2001/Sentimental-Analysis")
    model2 = AutoModelForSequenceClassification.from_pretrained("Dmyadav2001/Sentimental-Analysis")

    sentiment_analysis2 = pipeline("text-classification", model=model2, tokenizer=tokenizer2)
    
    
    # Initialize sentiment analysis pipeline
    sentiment_analysis = pipeline("text-classification", model=model, tokenizer=tokenizer)
    
    # Convert Pandas Series to list
    combined_texts = data['Combined'].tolist()

    predictions2 = sentiment_analysis2(combined_texts)
    
    # Predict sentiment and count positive/negative labels
    predictions = sentiment_analysis(combined_texts)
    #print(predictions)
    predicted_labels = [pred['label'] for pred in predictions]
    temp = []
    for pred in predictions:
        if pred['label'] == 'positive':
            temp.append("positive")
        else:
            temp.append("negative")
    data['Sentiment'] = temp
    pos3 = predicted_labels.count('positive')
    neg3 = predicted_labels.count('negative')

    pos2 = sum(1 for pred in predictions2 if  pred['label'] == 'LABEL_1')
    neg21 = sum(1 for pred in predictions2 if pred['label'] == 'LABEL_0')
    neg22 = sum(1 for pred in predictions2 if pred['label'] == 'LABEL_2')
    neg2=neg21+neg22
    

def perform_classification():
    dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data"
    file = get_max_numbered_csv(dir)
    dir = dir + "\\" + file
    df = pd.read_csv(dir)
    a=rameez(df)
    a=clean2(a)
    trans2(a)
    df.to_csv("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data Classified\\"+file)
    predict_and_evaluate(a)

#a.to_csv("C:\\Users\\praga\\Desktop\\aiproject\\Predicted_CSV\\Modified1030.csv",index=False)
#modified_df = pd.read_csv("C:\\Users\\praga\\Desktop\\aiproject\\Predicted_CSV\\Modified1030.csv")
#predicted_labels = modified_df['predicted_label']
#original_df = pd.read_csv(dir)
#original_df['predicted_label'] = predicted_labels
#original_df.to_csv(dir, index=False)

#############################
#perform_classification()
#print(pos3)
#print(neg3)
#print(pos2)
#print(neg2)
#print(pos1)
#print(neg1)
#############################