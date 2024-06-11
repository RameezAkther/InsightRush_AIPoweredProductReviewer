from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from WebScraper import productDetailAmazon
from WebScraper import amazonProductReviewScraper
from WebScraper import flipkartProductReviewPartial
from WebScraper import productDetailFlipkart
from WebScraper import productDetailGeneral
from WebScraper import getAmazonpgs
from WebScraper import getFlipkartpgs
from WebScraper import maxFile
from WebScraper import backgroundRemover
from SentimentSummarizer import classifier
from SentimentSummarizer import wordCloud
from SentimentSummarizer import summarizer
from datetime import date
import asyncio
import secrets
import threading
import ast
import mysql.connector
import atexit
import signal

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

searchURL = None

amazonProdInfo = {}
flipkartProdInfo = {}

genProdInfo = {}

ai = []

n = 0

img_lst = []

content1 = []
content2 = {}

content3 = None

image_dir = None

image_dir1 = None
image_dir2 = None
image_dir3 = None

numRev = 0
numPgs = 0
number_pgs = 0

seller = None

thread1 = None

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rameez",
    database="product_detail_two"
)

def finalContentAmazon():
    global image_dir1
    global image_dir2
    global image_dir3

    thread1.join()
    today = date.today()
    
    genProdInfo = productDetailGeneral.prodDetail
    if amazonProdInfo['Title'] == " ":
        if genProdInfo['Title'] == " ":
            content2['Title'] = "-"
        else:
            content2['Title'] = genProdInfo['Title']
    else:
        content2['Title'] = amazonProdInfo['Title']
    
    if genProdInfo['Highest Price'] == " ":
        content2['HighestPrice'] = "-"
    else:
        content2['HighestPrice'] = genProdInfo['Highest Price']
    
    if genProdInfo['Date of highest price'] == " ":
        content2['DateofHighestPrice'] = "-"
    else:
        content2['DateofHighestPrice'] = genProdInfo['Date of highest price']
    
    if genProdInfo['Lowest Price'] == " ":
        content2['LowestPrice'] = "-"
    else:
        content2['LowestPrice'] = genProdInfo['Lowest Price']
    
    if genProdInfo['Date of lowest price'] == " ":
        content2['DateofLowestPrice'] = "-"
    else:
        content2['DateofLowestPrice'] = genProdInfo['Date of lowest price']
    
    if genProdInfo['Average Price'] == " ":
        content2['AveragePrice'] = "-"
    else:
        content2['AveragePrice'] = genProdInfo['Average Price']
    
    if genProdInfo['Average Price as of'] == " ":
        content2['DateofAveragePrice'] = "-"
    else:
        content2['DateofAveragePrice'] = genProdInfo['Average Price as of']
    
    if amazonProdInfo['Current Price'] == " ":
        if genProdInfo['Current Price'] == " ":
            content2['CurrentPrice'] = "-"
        else:
            content2['CurrentPrice'] = genProdInfo['Current Price']
    else:
        content2['CurrentPrice'] = amazonProdInfo['Current Price']
    
    if genProdInfo['Label Price'] == " ":
        content2['LabelPrice'] = "-"
    else:
        content2['LabelPrice'] = genProdInfo['Label Price']
    
    if genProdInfo['Savings'] == " ":
        content2['Savings'] = "-"
    else:
        content2['Savings'] = genProdInfo['Savings']
    
    if genProdInfo['Discount'] == " ":
        content2['Discount'] = "-"
    else:
        content2['Discount'] = genProdInfo['Discount']
    
    if genProdInfo['Suggestion'] == " ":
        content2['Suggestion'] = "-"
    else:
        content2['Suggestion'] = genProdInfo['Suggestion']
    
    if genProdInfo['Status'] == " ":
        content2['Status'] = "-"
    else:
        content2['Status'] = genProdInfo['Status']
    
    if amazonProdInfo['Amazon AI'] == " ":
        content2['AmazonAI'] = "-"
    else:
        content2['AmazonAI'] = amazonProdInfo['Amazon AI']
    
    content2['NumRev'] = numRev
    content2['UsrNumRev'] = int(number_pgs)*10

    classifier.perform_classification()
    wordCloud.create_wordcloud()

    image_dir1 = wordCloud.d1
    image_dir2 = wordCloud.d2
    image_dir3 = wordCloud.d3

    content2['pos1'] = int(classifier.pos1)
    content2['pos2'] = int(classifier.pos2)
    content2['pos3'] = int(classifier.pos3)
    content2['neg1'] = int(classifier.neg1)
    content2['neg2'] = int(classifier.neg2)
    content2['neg3'] = int(classifier.neg3)

    summarizer.perform_summarize_on_df()

    content2['posSum'] = summarizer.positive_summary
    content2['negSum'] = summarizer.negative_summary
    content2['EposSum'] = summarizer.e_positive_summary
    content2['EnegSum'] = summarizer.e_negative_summary
    content2['About'] = amazonProdInfo['About']

    mycursor = db.cursor()
    name = content2['Title']
    name = " ".join(name.split()[:4])
    mycursor.execute("INSERT INTO Products (Name, Date, ImagePath, ImagePath1, ImagePath2, ImagePath3, origin) VALUES (%s, %s, %s, %s, %s, %s, %s)",(name,today,image_dir, image_dir1, image_dir2, image_dir3, 'amazon'))
    last_inserted_id = mycursor.lastrowid
    mycursor.execute("INSERT INTO PricingDetails (`Product ID`, Title, `Highest Price`, `Date of Highest Price`, `Lowest Price`, `Date of Lowest Price`, `Average Price`, `Date of Average Price`, `Current Price`, `Label Price`, Savings, Discount, Suggestion, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(last_inserted_id,content2['Title'],content2['HighestPrice'],content2['DateofHighestPrice'],content2['LowestPrice'],content2['DateofLowestPrice'],content2['AveragePrice'],content2['DateofAveragePrice'],content2['CurrentPrice'],content2['LabelPrice'],content2['Savings'],content2['Discount'],content2['Suggestion'],content2['Status']))
    mycursor.execute("INSERT INTO ReviewClassifier (`Product ID`, `CNN Positive`, `CNN Negative`, `LSTM Positive`, `LSTM Negative`, `Transformer Positive`, `Transformer Negative`, `Total Number of Reviews`, `Total number of Reviews Present in Web`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(last_inserted_id,content2['pos1'],content2['neg1'],content2['pos2'],content2['neg2'],content2['pos3'],content2['neg3'],content2['UsrNumRev'],content2['NumRev']))
    mycursor.execute("INSERT INTO ReviewSummary (`Product ID`, `Extractive Positive Summary`, `Extractive Negative Summary`, `Abstractive Positive Summary`, `Abstractive Negative Summary`, `Product detail`) VALUES (%s, %s, %s, %s, %s, %s)",(last_inserted_id,content2['EposSum'],content2['EnegSum'],content2['posSum'],content2['negSum'],str(content2['About'])))
    mycursor.execute("INSERT INTO AmazonSummary (`Product ID`, `Amazon Summary`) VALUES (%s, %s)",(last_inserted_id,content2['AmazonAI']))
    db.commit()
    mycursor.close()
    #db.close()
    print("Product Details of amazon are inserted successfully in the table")

def finalContentFlipkart():
    global image_dir1
    global image_dir2
    global image_dir3

    thread1.join()
    today = date.today()
    genProdInfo = productDetailGeneral.prodDetail
    if flipkartProdInfo['Title'] == " ":
        if genProdInfo['Title'] == " ":
            content2['Title'] = "-"
        else:
            content2['Title'] = genProdInfo['Title']
    else:
        content2['Title'] = flipkartProdInfo['Title']
    if genProdInfo['Highest Price'] == " ":
        content2['HighestPrice'] = "-"
    else:
        content2['HighestPrice'] = genProdInfo['Highest Price']
    if genProdInfo['Date of highest price'] == " ":
        content2['DateofHighestPrice'] = "-"
    else:
        content2['DateofHighestPrice'] = genProdInfo['Date of highest price']
    if genProdInfo['Lowest Price'] == " ":
        content2['LowestPrice'] = "-"
    else:
        content2['LowestPrice'] = genProdInfo['Lowest Price']
    if genProdInfo['Date of lowest price'] == " ":
        content2['DateofLowestPrice'] = "-"
    else:
        content2['DateofLowestPrice'] = genProdInfo['Date of lowest price']
    if genProdInfo['Average Price'] == " ":
        content2['AveragePrice'] = "-"
    else:
        content2['AveragePrice'] = genProdInfo['Average Price']
    if genProdInfo['Average Price as of'] == " ":
        content2['DateofAveragePrice'] = "-"
    else:
        content2['DateofAveragePrice'] = genProdInfo['Average Price as of']
    if flipkartProdInfo['Current Price'] == " ":
        if genProdInfo['Current Price'] == " ":
            content2['CurrentPrice'] = "-"
        else:
            content2['CurrentPrice'] = genProdInfo['Current Price']
    else:
        content2['CurrentPrice'] = flipkartProdInfo['Current Price']
    if genProdInfo['Label Price'] == " ":
        content2['LabelPrice'] = "-"
    else:
        content2['LabelPrice'] = genProdInfo['Label Price']
    if genProdInfo['Savings'] == " ":
        content2['Savings'] = "-"
    else:
        content2['Savings'] = genProdInfo['Savings']
    if genProdInfo['Discount'] == " ":
        content2['Discount'] = "-"
    else:
        content2['Discount'] = genProdInfo['Discount']
    if genProdInfo['Suggestion'] == " ":
        content2['Suggestion'] = "-"
    else:
        content2['Suggestion'] = genProdInfo['Suggestion']
    if genProdInfo['Status'] == " ":
        content2['Status'] = "-"
    else:
        content2['Status'] = genProdInfo['Status']
    content2['NumRev'] = numRev
    content2['UsrNumRev'] = int(number_pgs)*10

    classifier.perform_classification()
    wordCloud.create_wordcloud()

    image_dir1 = wordCloud.d1
    image_dir2 = wordCloud.d2
    image_dir3 = wordCloud.d3

    content2['pos1'] = int(classifier.pos1)
    content2['pos2'] = int(classifier.pos2)
    content2['pos3'] = int(classifier.pos3)
    content2['neg1'] = int(classifier.neg1)
    content2['neg2'] = int(classifier.neg2)
    content2['neg3'] = int(classifier.neg3)

    summarizer.perform_summarize_on_df()

    content2['posSum'] = summarizer.positive_summary
    content2['negSum'] = summarizer.negative_summary
    content2['EposSum'] = summarizer.e_positive_summary
    content2['EnegSum'] = summarizer.e_negative_summary

    content2['About'] = flipkartProdInfo['About']

    mycursor = db.cursor()
    name = content2['Title']
    name = " ".join(name.split()[:4])
    mycursor.execute("INSERT INTO Products (Name, Date, ImagePath, ImagePath1, ImagePath2, ImagePath3, origin) VALUES (%s, %s, %s, %s, %s, %s, %s)",(name,today,image_dir, image_dir1, image_dir2, image_dir3, 'flipkart'))
    last_inserted_id = mycursor.lastrowid
    mycursor.execute("INSERT INTO PricingDetails (`Product ID`, Title, `Highest Price`, `Date of Highest Price`, `Lowest Price`, `Date of Lowest Price`, `Average Price`, `Date of Average Price`, `Current Price`, `Label Price`, Savings, Discount, Suggestion, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(last_inserted_id,content2['Title'],content2['HighestPrice'],content2['DateofHighestPrice'],content2['LowestPrice'],content2['DateofLowestPrice'],content2['AveragePrice'],content2['DateofAveragePrice'],content2['CurrentPrice'],content2['LabelPrice'],content2['Savings'],content2['Discount'],content2['Suggestion'],content2['Status']))
    mycursor.execute("INSERT INTO ReviewClassifier (`Product ID`, `CNN Positive`, `CNN Negative`, `LSTM Positive`, `LSTM Negative`, `Transformer Positive`, `Transformer Negative`, `Total Number of Reviews`, `Total number of Reviews Present in Web`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(last_inserted_id,content2['pos1'],content2['neg1'],content2['pos2'],content2['neg2'],content2['pos3'],content2['neg3'],content2['UsrNumRev'],content2['NumRev']))
    mycursor.execute("INSERT INTO ReviewSummary (`Product ID`, `Extractive Positive Summary`, `Extractive Negative Summary`, `Abstractive Positive Summary`, `Abstractive Negative Summary`, `Product detail`) VALUES (%s, %s, %s, %s, %s, %s)",(last_inserted_id,content2['EposSum'],content2['EnegSum'],content2['posSum'],content2['negSum'],str(content2['About'])))
    db.commit()
    mycursor.close()
    #db.close()
    print("Product Details of flipkart are inserted successfully in the table")

def ContentHistoryAmazon(prod_id):
    global image_dir
    global image_dir1
    global image_dir2
    global image_dir3

    mycursor = db.cursor()
    product_id = prod_id

    prod = "SELECT * FROM Products WHERE `Product ID` = %s"
    mycursor.execute(prod, (product_id,))
    prod_meta_data = mycursor.fetchall()

    image_dir = prod_meta_data[0][3]
    image_dir1 = prod_meta_data[0][4]
    image_dir2 = prod_meta_data[0][5]
    image_dir3 = prod_meta_data[0][6]

    # Fetching data from AmazonSummary
    amazon_query = "SELECT * FROM AmazonSummary WHERE `Product ID` = %s"
    mycursor.execute(amazon_query, (product_id,))
    amazon_data = mycursor.fetchall()

    # Fetching data from PricingDetails
    pricing_query = "SELECT * FROM PricingDetails WHERE `Product ID` = %s"
    mycursor.execute(pricing_query, (product_id,))
    pricing_data = mycursor.fetchall()

    # Fetching data from ReviewClassifier
    classifier_query = "SELECT * FROM ReviewClassifier WHERE `Product ID` = %s"
    mycursor.execute(classifier_query, (product_id,))
    classifier_data = mycursor.fetchall()

    # Fetching data from ReviewSummary
    summary_query = "SELECT * FROM ReviewSummary WHERE `Product ID` = %s"
    mycursor.execute(summary_query, (product_id,))
    summary_data = mycursor.fetchall()
    
    mycursor.close()

    content2['Title'] = str(pricing_data[0][1])
    content2['HighestPrice'] = str(pricing_data[0][2])
    content2['DateofHighestPrice'] = str(pricing_data[0][3])
    content2["LowestPrice"] = str(pricing_data[0][4])
    content2['DateofLowestPrice'] = str(pricing_data[0][5])
    content2["AveragePrice"] = str(pricing_data[0][6])
    content2['DateofAveragePrice'] = str(pricing_data[0][7])
    content2['LabelPrice'] = str(pricing_data[0][8])
    content2['Savings'] = str(pricing_data[0][9])
    content2['Discount'] = str(pricing_data[0][10])
    content2['Suggestion'] = str(pricing_data[0][11])
    content2['Status'] = str(pricing_data[0][12])

    content2['pos1'] = str(classifier_data[0][1])
    content2['neg1'] = str(classifier_data[0][2])
    content2['pos2'] = str(classifier_data[0][3])
    content2['neg2'] = str(classifier_data[0][4])
    content2['pos3'] = str(classifier_data[0][5])
    content2['neg3'] = str(classifier_data[0][6])
    content2['NumRev'] = str(classifier_data[0][7])
    content2['UsrNumRev'] = str(classifier_data[0][8])

    content2['EposSum'] = str(summary_data[0][1])
    content2['EnegSum'] = str(summary_data[0][2])
    content2['posSum'] = str(summary_data[0][3])
    content2['negSum'] = str(summary_data[0][4])
    list_s = ast.literal_eval(summary_data[0][5])
    content2['About'] = list_s
    content2['AmazonAI'] = str(amazon_data[0][1])

def ContentHistoryFlipkart(prod_id):
    global image_dir
    global image_dir1
    global image_dir2
    global image_dir3

    mycursor = db.cursor()
    product_id = prod_id

    prod = "SELECT * FROM Products WHERE `Product ID` = %s"
    mycursor.execute(prod, (product_id,))
    prod_meta_data = mycursor.fetchall()

    image_dir = prod_meta_data[0][3]
    image_dir1 = prod_meta_data[0][4]
    image_dir2 = prod_meta_data[0][5]
    image_dir3 = prod_meta_data[0][6]
    
    # Fetching data from PricingDetails
    pricing_query = "SELECT * FROM PricingDetails WHERE `Product ID` = %s"
    mycursor.execute(pricing_query, (product_id,))
    pricing_data = mycursor.fetchall()

    # Fetching data from ReviewClassifier
    classifier_query = "SELECT * FROM ReviewClassifier WHERE `Product ID` = %s"
    mycursor.execute(classifier_query, (product_id,))
    classifier_data = mycursor.fetchall()

    # Fetching data from ReviewSummary
    summary_query = "SELECT * FROM ReviewSummary WHERE `Product ID` = %s"
    mycursor.execute(summary_query, (product_id,))
    summary_data = mycursor.fetchall()
    
    mycursor.close()

    content2['Title'] = str(pricing_data[0][1])
    content2['HighestPrice'] = str(pricing_data[0][2])
    content2['DateofHighestPrice'] = str(pricing_data[0][3])
    content2["LowestPrice"] = str(pricing_data[0][4])
    content2['DateofLowestPrice'] = str(pricing_data[0][5])
    content2["AveragePrice"] = str(pricing_data[0][6])
    content2['DateofAveragePrice'] = str(pricing_data[0][7])
    content2['LabelPrice'] = str(pricing_data[0][8])
    content2['Savings'] = str(pricing_data[0][9])
    content2['Discount'] = str(pricing_data[0][10])
    content2['Suggestion'] = str(pricing_data[0][11])
    content2['Status'] = str(pricing_data[0][12])

    content2['pos1'] = str(classifier_data[0][1])
    content2['neg1'] = str(classifier_data[0][2])
    content2['pos2'] = str(classifier_data[0][3])
    content2['neg2'] = str(classifier_data[0][4])
    content2['pos3'] = str(classifier_data[0][5])
    content2['neg3'] = str(classifier_data[0][6])
    content2['NumRev'] = str(classifier_data[0][7])
    content2['UsrNumRev'] = str(classifier_data[0][8])

    content2['EposSum'] = str(summary_data[0][1])
    content2['EnegSum'] = str(summary_data[0][2])
    content2['posSum'] = str(summary_data[0][3])
    content2['negSum'] = str(summary_data[0][4])
    list_s = ast.literal_eval(summary_data[0][5])
    content2['About'] = list_s


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/image')
def serve_image():
    global image_dir
    return send_file(image_dir, mimetype='image/png')

@app.route('/image1')
def serve_image_1():
    global image_dir1
    return send_file(image_dir1, mimetype='image/png')

@app.route('/image22') 
def serve_image_22():
    global image_dir2
    return send_file(image_dir2, mimetype='image/png')

@app.route('/image3')
def serve_image_3():
    global image_dir3
    return send_file(image_dir3, mimetype='image/png')

@app.route('/image2')
def serve_image_2():
    global n
    img = img_lst[n]
    n+=1
    #print(img)
    return send_file(img, mimetype='image/jpg')

@app.route('/submitURL', methods=['POST', 'GET'])
async def submit_URL():
    global numRev
    global numPgs
    global searchURL
    global amazonProdInfo
    global flipkartProdInfo
    global thread1
    global image_dir
    searchURL = request.form['searchURL']
    if 'amazon' in searchURL:
        try:
            loop = asyncio.get_event_loop()
            amazonProdInfo = await loop.run_in_executor(None, lambda: productDetailAmazon.ext(searchURL))
            thread1 = threading.Thread(target=productDetailGeneral.ext, args=(searchURL,))
            thread1.start()
            numRev = await loop.run_in_executor(None, lambda: getAmazonpgs.totalReview(searchURL))
            await loop.run_in_executor(None, lambda: backgroundRemover.remove_background())
            image_dir = "C:\\users\\ramee\\Desktop\\AI Lab\\Project\\Image"+"\\"+maxFile.get_max_numbered_png("C:\\users\\ramee\\Desktop\\AI Lab\\Project\\Image")
            numPgs = int(int(numRev) / 10) + 1
            content1.append(amazonProdInfo['Title'])
            content1.append(numRev)
            content1.append(numPgs)
            return redirect(url_for('get_number_pages'))
        except Exception as e:
            print(e)
            return redirect('/')
    elif 'flipkart' in searchURL:
        try:
            loop = asyncio.get_event_loop()
            flipkartProdInfo = await loop.run_in_executor(None, lambda: productDetailFlipkart.ext(searchURL))
            thread1 = threading.Thread(target=productDetailGeneral.ext, args=(searchURL,))
            thread1.start()
            await loop.run_in_executor(None, lambda: backgroundRemover.remove_background())
            numRev = await loop.run_in_executor(None, lambda: getFlipkartpgs.totalReviews(searchURL))
            image_dir = "C:\\users\\ramee\\Desktop\\AI Lab\\Project\\Image"+"\\"+maxFile.get_max_numbered_png("C:\\users\\ramee\\Desktop\\AI Lab\\Project\\Image")
            numPgs = int(int(numRev) / 10)
            content1.append(flipkartProdInfo['Title'])
            content1.append(numRev)
            content1.append(numPgs)
            return redirect(url_for('get_number_pages'))
        except Exception as e:
            print(e)
            return redirect('/')
    else:
        flash('Invalid URL. Please enter a valid URL.', 'error')
        return redirect('/')
    
@app.route('/pageNumbers', methods=['GET', 'POST'])
async def get_number_pages():
    global thread2
    global genProdInfo
    global number_pgs
    if request.method == "GET":
        return render_template('page1.html', content=content1)
    elif request.method == "POST":
        number_pgs = request.form['pgNum']
        if int(number_pgs) > numPgs or int(number_pgs) < 0:
            flash('Invalid number of pages. Please enter a valid number', 'error')
            return render_template('page1.html', content=content1)
        else:
            if "amazon" in searchURL:
                loop = asyncio.get_event_loop()
                thread2 = threading.Thread(target=amazonProductReviewScraper.get_review, args=(searchURL,int(number_pgs)))
                thread2.start()
                await loop.run_in_executor(None, lambda: finalContentAmazon())
                return render_template('page2Amazon.html', content=content2)
            elif "flipkart" in searchURL:
                loop = asyncio.get_event_loop()
                thread2 = threading.Thread(target=flipkartProductReviewPartial.get_review, args=(searchURL,number_pgs))
                thread2.start()
                await loop.run_in_executor(None, lambda: finalContentFlipkart())
                return render_template('page2Flipkart.html', content=content2)

@app.route('/history', methods=['POST', 'GET'])
async def history():
    global content3
    global seller
    if request.method == "GET":
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM Products")
        content3 = mycursor.fetchall()
        mycursor.close()
        for i in content3:
            img_lst.append(i[3])
        #print(img_lst)
        return render_template('history.html', content=content3)
    elif request.method == "POST":
        loop = asyncio.get_event_loop()
        product_id = request.form['productID']
        product_id = int(product_id)
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM Products WHERE `Product ID` = %s",(product_id,))
        origin = mycursor.fetchall()
        seller = str(origin[0][-1])
        if seller == "amazon":
            await loop.run_in_executor(None, lambda: ContentHistoryAmazon(product_id))
            return redirect('/historyInfo')
        else:
            await loop.run_in_executor(None, lambda: ContentHistoryFlipkart(product_id))
            return redirect('/historyInfo')

@app.route('/historyInfo')
def historyInfo(): 
    if seller == "amazon": 
        return render_template('page2Amazon.html',content=content2)
    else:
        return render_template('page2Flipkart.html',content=content2)


def close_db_connection():
    """Function to close the database connection."""
    if db.is_connected():
        db.close()
        print("Database connection closed.")

atexit.register(close_db_connection)

def signal_handler(signal, frame):
    """Signal handler for SIGINT to close the database connection."""
    close_db_connection()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    app.run(debug=True)