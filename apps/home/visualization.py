import sqlite3
from sqlite3 import Error
from flask import Flask, render_template
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from PIL import Image

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

def select_task_by_cluster(conn, cluster):
    """
    Query tasks by cluster
    :param conn: the Connection object
    :param cluster:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT wc FROM Clusters WHERE cluster=?", (cluster,))

    rows = cur.fetchall()

def main():
    database = r"F:\ppats\Website\flask dashboard\apps\db.sqlite3"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query task by cluster:")
        select_task_by_cluster(conn, 1)

       

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/word_cloud', methods=['GET'])
def word_cloud():
    cluster0 = select_task_by_cluster(conn, 0)
    comment_words = ''
    stopwords = set(STOPWORDS)

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
                            background_color ='purple',
                            colormap='Pastel1',
				            stopwords = stopwords,
				            min_font_size = 10).generate(comment_words)

        
plt.figure(figsize = (5, 5), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
plt.show()

if __name__ == '__main__':
    app.run(debug=True)