from transformers import BartForConditionalGeneration, BartTokenizer
import pandas as pd
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.tokenize import word_tokenize
from nltk.cluster.util import cosine_distance
import numpy as np
import google.generativeai as genai

genai_api = "AIzaSyA44RXOJCpwf1OTmxF_PDQOc0OCffcJlX4"

genai.configure(api_key=genai_api)


positive_summary = None
negative_summary = None
e_positive_summary = None
e_negative_summary = None

bart_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
bart_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

def preprocess_text(sentence):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(sentence.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

def sentence_similarity(sent1, sent2):
    words1 = preprocess_text(sent1)
    words2 = preprocess_text(sent2)
    all_words = list(set(words1 + words2))
    vector1 = [1 if word in words1 else 0 for word in all_words]
    vector2 = [1 if word in words2 else 0 for word in all_words]
    return 1 - cosine_distance(vector1, vector2)

def build_similarity_matrix(sentences):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if i != j:
                similarity_matrix[i][j] = sentence_similarity(sentences[i], sentences[j])
    return similarity_matrix

def generate_summary(text, num_sentences):
    sentences = sent_tokenize(text)
    sentence_similarity_matrix = build_similarity_matrix(sentences)
    scores = np.sum(sentence_similarity_matrix, axis=1)
    ranked_sentences = sorted(((scores[i], sentence) for i, sentence in enumerate(sentences)), reverse=True)
    summary = ' '.join([sentence for score, sentence in ranked_sentences[:num_sentences]])
    return summary



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

def summarize_text(text, model, tokenizer, max_length=200, min_length=40):
    inputs = tokenizer([text], max_length=1024, truncation=True, return_tensors='pt')
    summary_ids = model.generate(inputs['input_ids'], max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def perform_summarize_on_df():
    global positive_summary
    global negative_summary
    global e_positive_summary
    global e_negative_summary

    dir = get_max_numbered_csv("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data Classified")
    df = pd.read_csv("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data Classified\\"+ dir)

    positive_reviews = " ".join(df[df['Sentiment'] == 'positive']['Review Body'])
    negative_reviews = " ".join(df[df['Sentiment'] == 'negative']['Review Body'])

    model = genai.GenerativeModel('gemini-1.5-flash')
    
    positive_summary = summarize_text(positive_reviews, bart_model, bart_tokenizer)
    #print("\nPositive Reviews Summary:\n", positive_summary)

    # Summarize negative reviews
    negative_summary = summarize_text(negative_reviews, bart_model, bart_tokenizer)
    #print("\nNegative Reviews Summary:\n", negative_summary)

    response1 = model.generate_content("Here is an abstractive summary of a product's review now modify it so that it reads out like third person view"+positive_summary)
    positive_summary = response1.text

    response2 = model.generate_content("Here is an abstractive summary of a product's review now modify it so that it reads out like third person view"+negative_summary)
    negative_summary = response2.text

    e_negative_summary = generate_summary(negative_reviews, 2)
    e_positive_summary = generate_summary(positive_reviews, 2)


############################
#perform_summarize_on_df()
#print(positive_summary)
#print(negative_summary)
#print(e_negative_summary)
#print(e_positive_summary)
############################