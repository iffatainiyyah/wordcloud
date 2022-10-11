import sqlite3
from sqlite3 import Error
from flask import Flask, render_template
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io
import urllib
import base64
import random
import re
import numpy as np

app = Flask(__name__)



def home_page():
    return render_template('index.html')


def symbol_wc(df, column,cluster):

    # Get Data
    cluster0 = df.loc[df[column] == cluster]
    words = ''
    stopwords = set(STOPWORDS)


    for val in cluster0:

        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        words += " ".join(tokens)+" "
        
        
    wordcloud = WordCloud(width = 1200, height = 800,
                            background_color = '#FFFDE3',
                            colormap='tab10',
				            stopwords = stopwords,
                            regexp = r"[Pp]s[0-9](?:[\(]?[0-9]*[\)]?)?(?:[\(]?[0-9]*[\)]?)? ? ?[a-zA-Z]?",
				            min_font_size = 16).generate(words)

        
    plt.figure(figsize = (5, 5), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    # plt.savefig('generated_plots.png')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    return plot_data


def grouped_wc(df,column,cluster):

    # Get Data
    cluster0 = df.loc[df[column] == cluster]
    grouped_words = []
    dictionary = {}
    stopwords = set(STOPWORDS)


    for val in cluster0:

        # typecaste each val to string
        vals = val[0]

        # split the value and grouped 3 words
        tokens = vals.split()
        grouped_words += [' '.join(tokens[i: i + 3]) for i in range(0, len(tokens), 3)]

       # Converts each words into lowercase
        for i in range(len(grouped_words)):
            grouped_words[i] = grouped_words[i].lower()
            # grouped_words[i] = re.sub(r'[^\w\s\,]', '', grouped_words[i])
            grouped_words[i] = grouped_words[i].replace(',','')
        
    for word in grouped_words:
        if word not in dictionary.keys():
            dictionary[word] = 1
        else:
            dictionary[word] += 1

    cloud = WordCloud(width = 1200, height = 800,
                            background_color = '#FFFDE3',
                            colormap='tab10',
				            stopwords = stopwords,
				            min_font_size = 16)
    cloud.generate_from_frequencies(dictionary)

        
    plt.figure(figsize = (5, 5), facecolor = None)
    plt.imshow(cloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    # plt.savefig('generated_plots.png')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    return plot_data


def vehicle_wc(df,column,cluster):

    # Get Data
    cluster0 = df.loc[df[column] == cluster]
    words = ''
    stopwords = set(STOPWORDS)

    for val in cluster0:

        
        vals = val[0]

        # split the value
        tokens = vals.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        words += " ".join(tokens)+" "
        
        
    wordcloud = WordCloud(width = 1200, height = 800,
                            background_color = '#FFFDE3',
                            colormap='tab10',
				            stopwords = stopwords,
                            # regexp=r"[a-z]{0,10}?[a-z]{0,10}",
				            min_font_size = 10).generate(words)

        
    plt.figure(figsize = (5, 5), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    # plt.savefig('generated_plots.png')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_data = urllib.parse.quote(base64.b64encode(img.getvalue()).decode('utf-8'))
    return plot_data

def regex_split(series, pattern):
    data = []
    
    for row in series:
        list_pasal = []
        for pasal in row:
            result = re.findall(pattern, pasal)
            #print(pasal)
            list_pasal.append(result[0].strip())        

        data.append(list_pasal)
  
    return data

def one_hot(df, nama_pasal):
    data = {}
    for list_of_hukuman in df[nama_pasal]:
        for pasal in list_of_hukuman:
            if pasal not in data.keys():
                data[pasal] = []
                
                for list_hukuman in df[nama_pasal]:
                    if pasal in list_hukuman:
                        data[pasal].append(1)
                    else:
                        data[pasal].append(0)

    for key, value in data.items():
        df[key] = value
    return df

def euclideanDistance (x,y):
  squared_ed = 0
  for i in range (len(x)):
    squared_ed += (x[i] - y[i])**2
  ed = np.sqrt(squared_ed)
  return ed

def prediksi(medoid, data):
    pred = []

    for i in range (len(data)):
      # Jarak dari poin data ke setiap medoids
      ed_list = []
      
      for j in range(len(medoid)):
        ed_list.append(euclideanDistance(medoid[j], data[i] ))

      pred.append(ed_list.index(min(ed_list)))

    return np.array(pred)
    

if __name__ == "__main__":
    app.run(debug=True)