import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

d1 = None
d2 = None
d3 = None

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

def get_max_numbered_jpg(directory):
    files = os.listdir(directory)
    max_number = float('-inf')
    max_filename = None
    for file_name in files:
        if file_name.endswith('.jpg'):
            try:
                file_number = int(os.path.splitext(file_name)[0])
                if file_number > max_number:
                    max_number = file_number
                    max_filename = file_name
            except ValueError:
                continue
    return max_number

def create_wordcloud():
    global d1
    global d2
    global d3

    dir = get_max_numbered_csv("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data Classified")
    df = pd.read_csv("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data Classified\\"+ dir)

    dir_img = get_max_numbered_jpg("C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\UI\\static\\Images\\Wordcloud1")

    d1 = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\UI\\static\\Images\\Wordcloud1\\"
    d2 = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\UI\static\\Images\\Wordcloud2\\"
    d3 = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\UI\\static\\Images\\Wordcloud3\\"

    text = ' '.join(df['Review Body'].dropna())
    text1 = ' '.join(df[df['Sentiment'] == 'negative']['Review Body'].dropna())
    text2 = ' '.join(df[df['Sentiment'] == 'positive']['Review Body'].dropna())

    if len(text1) == 0:
        text1 = "nothing nothing"
    if len(text2) == 0:
        text2 = "nothing nothing"
    if len(text) == 0:
        text = "nothin nothin"

    wordcloud = WordCloud(width=800, height=400, background_color='rgba(255, 255, 255, 0)').generate(text)
    wordcloud2 = WordCloud(width=800, height=400, background_color='rgba(255, 255, 255, 0)').generate(text1)
    wordcloud3 = WordCloud(width=800, height=400, background_color='rgba(255, 255, 255, 0)').generate(text2)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title("Overall Body Word Cloud")
    d1 = d1 + str(dir_img+1) + ".jpg"
    plt.savefig(d1)  # Save wordcloud image to d1 directory

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud2, interpolation='bilinear')
    plt.axis('off')
    plt.title("Negative Body Word Cloud")
    d2 = d2 + str(dir_img+1) + ".jpg"
    plt.savefig(d2)  # Save wordcloud1 image to d2 directory

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud3, interpolation='bilinear')
    plt.axis('off')
    plt.title("Positive Body Word Cloud")
    d3 = d3 + str(dir_img+1) + ".jpg"
    plt.savefig(d3)  # Save wordcloud2 image to d3 directory

#create_wordcloud()