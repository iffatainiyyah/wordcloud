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

def select_task_by_cluster(conn, columns, cluster, table):
    """
    Query tasks by cluster
    :param conn: the Connection object
    :param columns, cluster, table:
    :return:
    """
    cur = conn.cursor()
    # cur.execute("SELECT wc FROM " + table + " WHERE clusters=?", (cluster,))
    cur.execute("SELECT " + columns + " FROM " + table + " WHERE cluster=?", (cluster,))

    rows = cur.fetchall()
    return rows

def select_task_for_vehicle(conn, columns, cluster):
    """
    Query tasks by cluster
    :param conn: the Connection object
    :param columns, cluster:
    :return:
    """
    cur = conn.cursor()
    # cur.execute("SELECT wc FROM " + table + " WHERE clusters=?", (cluster,))
    cur.execute("SELECT " + columns + " FROM Cluster_a WHERE cluster=?", (cluster,))

    rows = cur.fetchall()
    return rows


@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/symbol_wc')
def symbol_wc(columns, cluster, table):
    # create a database connection
    database = r"F:\skripsi\Website\flask dashboard\apps\db.sqlite3"
    conn = create_connection(database)

    # Get Data
    cluster0 = select_task_by_cluster(conn, columns, cluster, table)
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
        
        
    wordcloud = WordCloud(width = 800, height = 800,
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

@app.route('/grouped_wc')
def grouped_wc(columns, cluster, table):
    # create a database connection
    database = r"F:\skripsi\Website\flask dashboard\apps\db.sqlite3"
    conn = create_connection(database)

    # Get Data
    cluster0 = select_task_by_cluster(conn, columns, cluster, table)
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

    cloud = WordCloud(width = 1200, height = 500,
                            background_color = '#400D51',
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

@app.route('/vehicle_wc')
def vehicle_wc(columns, cluster):
    # create a database connection
    database = r"F:\skripsi\Website\flask dashboard\apps\db.sqlite3"
    conn = create_connection(database)

    # Get Data
    cluster0 = select_task_for_vehicle(conn, columns, cluster)
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
        
        
    wordcloud = WordCloud(width = 800, height = 800,
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

if __name__ == '__main__':
    app.run(debug=True)