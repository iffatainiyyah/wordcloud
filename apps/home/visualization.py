import sqlite3
from sqlite3 import Error
from flask import Flask, render_template
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import io
import urllib
import base64
import random



app = Flask(__name__)

def create_connection(db):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)

    return conn

def select_task_by_cluster(conn, cluster, table):
    """
    Query tasks by cluster
    :param conn: the Connection object
    :param cluster:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT wc FROM " + table + " WHERE clusters=?", (cluster,))

    rows = cur.fetchall()
    return rows

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/word_cloud')
def word_cloud(cluster, table):
    # create a database connection
    database = r"F:\skripsi\Website\flask dashboard\apps\db.sqlite3"
    conn = create_connection(database)

    # Get Data
    cluster0 = select_task_by_cluster(conn, cluster, table)
    comment_words = ''
    stopwords = set(STOPWORDS)

    # Random Color

    for val in cluster0:

        # typecaste each val to string
        val = str(val)

        # split the value
        tokens = val.split()

        # Converts each token into lowercase
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        
        comment_words += " ".join(tokens)+" "
        
    wordcloud = WordCloud(width = 800, height = 800,
                            background_color = '#F5F5DC',
                            colormap='tab10',
				            stopwords = stopwords,
				            min_font_size = 10).generate(comment_words)

        
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

if __name__ == '__main__':
    app.run(debug=True)