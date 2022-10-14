# -*- encoding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from apps.home.website import regex_split, one_hot, euclideanDistance, prediksi
from apps.home.kmedoids import k_medoids
from apps.home import blueprint
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_required
from jinja2 import TemplateNotFound
import sqlite3
import os
import pandas as pd
import numpy as np
import re
import io
import urllib
import base64
import pickle
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA 
from wordcloud import WordCloud, STOPWORDS


UPLOAD_FOLDER = '/file'
ALLOWED_EXTENSIONS = {'csv', 'xls','xlsx'}
sqlites = r"F:\skripsi\Website\flask dashboard\apps\db.sqlite3"
data_pelanggaran = pd.read_excel('/Skripsi/Website/flask dashboard/apps/file/dataset test.xlsx')
data_prepro = None
dt_pca_80 = None
data_numeric = None
data_visual = None
predict_cluster = None
app = Flask(__name__)

@blueprint.route('/index.html')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route("/datapelanggaran.html", methods=['GET','POST'])
@login_required
def datapelanggaran():
    if request.method == 'POST':
        return redirect(url_for('home_blueprint.preprocessing'))
    return render_template('home/datapelanggaran.html',segment='pelanggaran', data_pelanggaran=data_pelanggaran)    

app.config['UPLOAD_FOLDER'] = '/Skripsi/Website/flask dashboard/apps/file'
@blueprint.route('/addData.html',  methods=['GET','POST'])
@login_required
def uploadFile():
    # global data_pelanggaran
    if request.method == 'POST':
        if request.files:
            file = request.files["file"]           
            msg="File already saved"
            ext = file.filename.rsplit('.', 1)[1].lower()
            acceptedExt = ['csv','xls','xlsx']
            if ext in acceptedExt:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],'dataset test.xlsx'))
        
        # path = "/Skripsi/Website/flask dashboard/apps/file/"+(file.filename)
        # if ext == "csv":
        #     data_pelanggaran = pd.read_csv(path)
        # else:
        #     data_pelanggaran = pd.read_excel(path)
        
    
        
        return redirect(url_for('home_blueprint.datapelanggaran'))
        #return render_template('home/datapelanggaran.html', data=data)
    
    return render_template('home/addData.html', segment='upload')

@blueprint.route('/praproses.html', methods=['GET','POST'])
@login_required
def preprocessing():
     
    if request.method == 'POST':
        return redirect(url_for('home_blueprint.clustering'))
    
    global dt_pca_80
    global data_numeric
    global data_prepro
    global data_pelanggaran

    data_pelanggaran = pd.DataFrame(data_pelanggaran)
    print('ini data pelanggaran :',data_pelanggaran)
    data_prepro = data_pelanggaran.copy()

    # Split data
    data_prepro['pasal_hukuman'] = data_prepro['pasal_hukuman'].str.split(',')
    data_prepro['pasal_tuntutan'] = data_prepro['pasal_tuntutan'].str.split(',')

    # Filtering data using regex
    pattern = r"[Pp]asal [0-9]+ ?(?:ay(?:at)?\.?)? ?(?:[\(]?[0-9]*[\)]?)? ?(?:huruf)? ?(?!jo)(?!dan)(?!atau)[a-zA-Z]?"
    pasal_hukuman_series = regex_split(data_prepro['pasal_hukuman'], pattern)
    pasal_tuntutan_series = regex_split(data_prepro['pasal_tuntutan'], pattern)

    data_prepro['pasal_hukuman'] = pasal_hukuman_series
    data_prepro['pasal_tuntutan'] = pasal_tuntutan_series
    print('ini hasil upload',data_prepro)

    data_numeric = data_prepro.copy()
    # One Hot Encoding data
    data_numeric = one_hot(data_numeric, 'pasal_hukuman')
    data_numeric = one_hot(data_numeric, 'pasal_tuntutan')

    data_numeric.drop('pasal_hukuman', axis=1, inplace=True)
    data_numeric.drop('pasal_tuntutan',axis=1, inplace=True)
    
    
    # Label Encoder 
    jenis_kendaraan_dict = {'JEEP': 0, 'LAIN-LAIN': 1, 'MINI BUS': 2, 'MKL/MOBIL PENUMPANG': 3, 'MOBIL BARANG/PICK UP': 4, 'SEDAN': 5, 
                        'SEPEDA MOTOR': 6, 'TRUCK BESAR': 7, 'TRUCK KECIL': 8, 'TRUCK TANGKI': 9}

    data_numeric['jenis_kendaraan'] = data_numeric.jenis_kendaraan.map(jenis_kendaraan_dict)
    
    # Normalisasi
    scaler = MinMaxScaler()
    scaler.fit(data_numeric)
    scaled_data = scaler.transform(data_numeric)

    # PCA
    pca_80 = PCA(n_components=7)
    dt_pca_80 = pca_80.fit_transform(scaled_data)

    print(data_numeric)
    
        
    return render_template('home/praproses.html', segment='pelanggaran', data_numeric = data_numeric)

@blueprint.route('/resultCluster.html', methods=['GET','POST'])
@login_required
def clustering():
    
    if request.method == 'POST':
        return redirect(url_for('home_blueprint.datacluster'))

    global predict_cluster
    global dt_pca_80
    global data_numeric
    
    data_numeric = pd.DataFrame(data_numeric)
    
    
    # load medoids from pickle
    file = open('/Skripsi/Website/flask dashboard/apps/file/Medoid_sc.pickle','rb')
    medoid_80 = pickle.load(file)
    

    # insert data to function 
    predict_cluster = prediksi(medoid_80, dt_pca_80)
    print("predict:", predict_cluster)
    data_numeric['cluster'] = predict_cluster
    print(data_numeric)

    return render_template('home/resultCluster.html', segment='pelanggaran', data_numerics=data_numeric)

@blueprint.route('/dataCluster.html', methods=['GET','POST'])
@login_required
def datacluster():
    global data_prepro
    global predict_cluster
    global data_visual
    # Rename data pasal
    data_prepro = pd.DataFrame(data_prepro)
    data_visual = data_prepro.copy()
    # print('testeu:',data_visual)

    # Split data hukuman
    data_hukuman = {
        'pasal_hukuman_1': [],
        'pasal_hukuman_2': [],
    }

    for split in data_visual['pasal_hukuman']:
        pasal_hukuman_1 = []
        pasal_hukuman_2 = []
        
        pasal_hukuman_1.append(split[0])
        try:
            pasal_hukuman_2.append(split[1])
        except IndexError:
            pasal_hukuman_2.append(0)
        data_hukuman['pasal_hukuman_1'].append(pasal_hukuman_1)
        data_hukuman['pasal_hukuman_2'].append(pasal_hukuman_2)

    data_visual['pasal_hukuman_1'] = data_hukuman['pasal_hukuman_1']
    data_visual['pasal_hukuman_2'] = data_hukuman['pasal_hukuman_2']
    

    # Split data tuntutan
    data_tuntutan = {
        'pasal_tuntutan_1': [],
        'pasal_tuntutan_2': [],
    }

    for split in data_visual['pasal_tuntutan']:
        pasal_tuntutan_1 = []
        pasal_tuntutan_2 = []
        
        pasal_tuntutan_1.append(split[0])
        try:
            pasal_tuntutan_2.append(split[1])
        except IndexError:
            pasal_tuntutan_2.append(0)
        data_tuntutan['pasal_tuntutan_1'].append(pasal_tuntutan_1)
        data_tuntutan['pasal_tuntutan_2'].append(pasal_tuntutan_2)

    data_visual['pasal_tuntutan_1'] = data_tuntutan['pasal_tuntutan_1']
    data_visual['pasal_tuntutan_2'] = data_tuntutan['pasal_tuntutan_2']

    data_visual.drop('pasal_hukuman', axis=1, inplace=True)
    data_visual.drop('pasal_tuntutan', axis=1, inplace=True)

    data_visual['pasal_tuntutan_1'] = [''.join(map(str, l)) for l in data_visual['pasal_tuntutan_1']]
    data_visual['pasal_tuntutan_2'] = [''.join(map(str, l)) for l in data_visual['pasal_tuntutan_2']]

    data_visual['pasal_hukuman_1'] = [''.join(map(str, l)) for l in data_visual['pasal_hukuman_1']]
    data_visual['pasal_hukuman_2'] = [''.join(map(str, l)) for l in data_visual['pasal_hukuman_2']]
    
    # read data for make dict to rename pasal
    rename_pasal = pd.read_excel("/Skripsi/Website/flask dashboard/apps/file/Pasal_singkatan.xlsx")
    rn_dict = dict(rename_pasal.values)
    
    data_visual['pasal_hukuman_1'] = data_visual['pasal_hukuman_1'].map(rn_dict)
    data_visual['pasal_hukuman_2'] = data_visual['pasal_hukuman_2'].map(rn_dict)
    data_visual['pasal_tuntutan_1'] = data_visual['pasal_tuntutan_1'].map(rn_dict)
    data_visual['pasal_tuntutan_2'] = data_visual['pasal_tuntutan_2'].map(rn_dict)
    
    # insert result rename data to dataframe
    data_visual['pasal_hukuman'] = np.where(data_visual['pasal_hukuman_2'].isnull(), data_visual['pasal_hukuman_1'], 
                                data_visual['pasal_hukuman_1']+', '+ data_visual['pasal_hukuman_2'])

    data_visual['pasal_tuntutan'] = np.where(data_visual['pasal_tuntutan_2'].isnull(), data_visual['pasal_tuntutan_1'], 
                                data_visual['pasal_tuntutan_1']+', '+ data_visual['pasal_tuntutan_2'])
    
     # Rename value jenis kendaraan
    data_visual['jenis_kendaraan'].replace(to_replace={'MOBIL BARANG/PICK UP':'MOBIL BARANG', 'LAIN-LAIN':'LAINNYA','MKL/MOBIL PENUMPANG':'MOBIL PENUMPANG', 
                                           'TRUCK BESAR':'TRUK BESAR', 'TRUCK KECIL':'TRUK KECIL', 'TRUCK TANGKI':'TRUK TANGKI'}, inplace= True)
    
    data_visual.drop('pasal_tuntutan_1', axis=1, inplace=True)
    data_visual.drop('pasal_tuntutan_2', axis=1, inplace=True)
    data_visual.drop('pasal_hukuman_1', axis=1, inplace=True)
    data_visual.drop('pasal_hukuman_2', axis=1, inplace=True)

    data_visual['cluster'] = predict_cluster
    
    
    return render_template('home/dataCluster.html', segment='pelanggaran', data_visual=data_visual)

def symbols_wc(columnn,cluster):
    global data_visual
    data_visual = pd.DataFrame(data_visual)

    # Get Data
    cluster = int(cluster)
    cluster0 = data_visual.loc[data_visual['cluster'] == cluster]
    cluster1 = cluster0[columnn].tolist()
    stopwords = set(STOPWORDS)

    dictionary={}
    for word in cluster1:
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


def vehicles_wc(column,cluster):
    global data_visual
    data_visual = pd.DataFrame(data_visual)

    # Get Data
    cluster = int(cluster)
    cluster0 = data_visual.loc[data_visual['cluster'] == cluster]
    cluster1 = cluster0[column]
    words = ''
    stopwords = set(STOPWORDS)


    for val in cluster1:

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

@blueprint.route('/form-wc.html', methods=['GET','POST'])
@login_required
def wcs():
    if request.method == 'POST':
        columns = request.form.get('column')
        clusters = request.form.get('cluster')
        details_t = ["Pasal 106 ayat (5) huruf a = Pada saat diadakan pemeriksaan Kendaraan Bermotor di Jalan setiap orang yang mengemudikan Kendaraan Bermotor wajib menunjukkan Surat Tanda Nomor Kendaraan Bermotor atau Surat Tanda Coba Kendaraan Bermotor.", "Pasal 106 ayat (5) huruf b = Pada saat diadakan pemeriksaan Kendaraan Bermotor di Jalan setiap orang yang mengemudikan Kendaraan Bermotor wajib menunjukkan Surat Izin Mengemudi (SIM).", "Pasal 77 ayat (1) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib memiliki Surat Izin Mengemudi sesuai dengan jenis Kendaraan Bermotor yang dikemudikan.", "Pasal 106 ayat (4) huruf c = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan Alat Pemberi Isyarat Lalu Lintas.", "Pasal 68 ayat (1) = Setiap Kendaraan Bermotor yang dioperasikan di Jalan wajib dilengkapi dengan Surat Tanda Nomor Kendaraan Bermotor dan Tanda Nomor Kendaraan Bermotor.", "Pasal 106 ayat (4) huruf a =  Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan rambu perintah atau rambu larangan dan Pasal 106 ayat (4) huruf b =  Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan Marka Jalan. ", "Pasal 106 ayat (6) = Setiap orang yang mengemudikan Kendaraan Bermotor beroda empat atau lebih di Jalan dan penumpang yang duduk di sampingnya wajib mengenakan sabuk keselamatan. ", "Pasal 106 ayat (8) = Setiap orang yang mengemudikan Sepeda Motor dan Penumpang Sepeda Motor wajib mengenakan helm yang memenuhi standar nasional Indonesia.", "Pasal 106 ayat (3) =Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan tentang persyaratan teknis dan laik jalan dan Pasal 106 ayat (5) huruf c = Pada saat diadakan pemeriksaan Kendaraan Bermotor di Jalan setiap orang yang mengemudikan Kendaraan Bermotor wajib menunjukkan bukti lulus uji berkala "]
        details_h = ["Pasal 288 ayat (1) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak dilengkapi dengan Surat Tanda Nomor Kendaraan Bermotor atau Surat Tanda Coba Kendaraan Bermotor yang ditetapkan oleh Kepolisian Negara Republik Indonesia sebagaimana dimaksud dalam Pasal 106 ayat (5) huruf a dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 288 ayat (2) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak dapat menunjukkan Surat Izin Mengemudi yang sah sebagaimana dimaksud dalam Pasal 106 ayat (5) huruf b dipidana dengan pidana kurungan paling lama 1 (satu) bulan dan/atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah).", "Pasal 281 = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak memiliki Surat Izin Mengemudi sebagaimana dimaksud dalam Pasal 77 ayat (1) dipidana dengan pidana kurungan paling lama 4 (empat) bulan atau denda paling banyak Rp1.000.000,00 (satu juta rupiah).", "Pasal 287 ayat (2) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang melanggar aturan perintah atau larangan yang dinyatakan dengan Alat Pemberi Isyarat Lalu Lintas sebagaimana dimaksud dalam Pasal 106 ayat (4) huruf c dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 280 = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak dipasangi Tanda Nomor Kendaraan Bermotor yang ditetapkan oleh Kepolisian Negara Republik Indonesia sebagaimana dimaksud dalam Pasal 68 ayat (1) dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 287 ayat (1) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang melanggar aturan perintah atau larangan yang dinyatakan dengan Rambu Lalu Lintas sebagaimana dimaksud dalam Pasal 106 ayat (4) huruf a atau Marka Jalan sebagaimana dimaksud dalam Pasal 106 ayat (4) huruf b dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 289 = Setiap orang yang mengemudikan Kendaraan Bermotor atau Penumpang yang duduk di samping Pengemudi yang tidak mengenakan sabuk keselamatan sebagaimana dimaksud dalam Pasal 106 ayat (6) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah).", "Pasal 291 ayat (1) = Setiap orang yang mengemudikan Sepeda Motor tidak mengenakan helm standar nasional Indonesia sebagaimana dimaksud dalam Pasal 106 ayat (8) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah) dan Pasal 291 ayat (2) = Setiap orang yang mengemudikan Sepeda Motor yang membiarkan penumpangnya tidak mengenakan helm sebagaimana dimaksud dalam Pasal 106 ayat (8) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah).", "Pasal 285 ayat (1) = Setiap orang yang mengemudikan Sepeda Motor di Jalan yang tidak memenuhi persyaratan teknis dan laik jalan yang meliputi kaca spion, klakson, lampu utama, lampu rem, lampu penunjuk arah, alat pemantul cahaya, alat pengukur kecepatan, knalpot, dan kedalaman alur ban sebagaimana dimaksud dalam Pasal 106 ayat (3) juncto Pasal 48 ayat (2) dan ayat (3) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah) dan Pasal 288 ayat (3) = Setiap orang yang mengemudikan mobil penumpang umum, mobil bus, mobil barang, kereta gandengan, dan kereta tempelan yang tidak dilengkapi dengan surat keterangan uji berkala dan tanda lulus uji berkala sebagaimana dimaksud dalam Pasal 106 ayat (5) huruf c dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah)."]

        # condition for input
        if columns == 'pasal_hukuman':
            result = symbols_wc(columns, clusters)
        elif columns == 'pasal_tuntutan':
            result = symbols_wc(columns, clusters)
        elif columns == 'jenis_kendaraan':
            result = vehicles_wc(columns, clusters)
        
        # condition for details pasal tuntutan
        if columns == 'pasal_tuntutan' and clusters == '0':
            details = details_t[0]
        elif columns == 'pasal_tuntutan' and clusters == '1':
            details = details_t[1]
        elif columns == 'pasal_tuntutan' and clusters == '2':
            details = details_t[2]
        elif columns == 'pasal_tuntutan' and clusters == '3':
            details = details_t[3]
        elif columns == 'pasal_tuntutan' and clusters == '4':
            details = details_t[4]
        elif columns == 'pasal_tuntutan' and clusters == '5':
            details = details_t[5]
        elif columns == 'pasal_tuntutan' and clusters == '6':
            details = details_t[6]
        elif columns == 'pasal_tuntutan' and clusters == '7':
            details = details_t[7]
        elif columns == 'pasal_tuntutan' and clusters == '8':
            details = details_t[8]

        
        # condition for details pasal hukuman
        if columns == 'pasal_hukuman' and clusters == '0':
            details = details_h[0]
        elif columns == 'pasal_hukuman' and clusters == '1':
            details = details_h[1]
        elif columns == 'pasal_hukuman' and clusters == '2':
            details = details_h[2]
        elif columns == 'pasal_hukuman' and clusters == '3':
            details = details_h[3]
        elif columns == 'pasal_hukuman' and clusters == '4':
            details = details_h[4]
        elif columns == 'pasal_hukuman' and clusters == '5':
            details = details_h[5]
        elif columns == 'pasal_hukuman' and clusters == '6':
            details = details_h[6]
        elif columns == 'pasal_hukuman' and clusters == '7':
            details = details_h[7]
        elif columns == 'pasal_hukuman' and clusters == '8':
            details = details_h[8]
        
        # condition for details jenis kendaraan
        if columns == 'jenis_kendaraan':
            details = ''
        


        return render_template('home/form-wc.html', plot_forms = result, plot_details = details, plot_columns = columns,
                                plot_clusters = clusters, segment="form")

    return render_template('home/form.html', plot_forms, plot_details, segment="form")



@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

