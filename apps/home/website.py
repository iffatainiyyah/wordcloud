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





def home_page():
    return render_template('index.html')


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
    

