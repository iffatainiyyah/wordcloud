# -*- encoding: utf-8 -*-


from apps.home.visualization import symbol_wc, grouped_wc, vehicle_wc
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')

@blueprint.route('/word-cloud.html')
@login_required
def wc():
    # symbol_wc(cluster ke berapa, nama tabelnya)
    # word cloud singkatan
    plot_data_0a = symbol_wc("pasal_tuntutan", 0, "Cluster_s")
    plot_data_1a = symbol_wc("pasal_tuntutan", 1, "Cluster_s")
    plot_data_2a = symbol_wc("pasal_tuntutan", 2, "Cluster_s")
    plot_data_3a = symbol_wc("pasal_tuntutan", 3, "Cluster_s")
    plot_data_4a = symbol_wc("pasal_tuntutan", 4, "Cluster_s")
    plot_data_5a = symbol_wc("pasal_tuntutan", 5, "Cluster_s")
    plot_data_6a = symbol_wc("pasal_tuntutan", 6, "Cluster_s")
    plot_data_7a = symbol_wc("pasal_tuntutan", 7, "Cluster_s")
    plot_data_8a = symbol_wc("pasal_tuntutan", 8, "Cluster_s")

    plot_data_0b = symbol_wc("pasal_hukuman", 0, "Cluster_s")
    plot_data_1b = symbol_wc("pasal_hukuman", 1, "Cluster_s")
    plot_data_2b = symbol_wc("pasal_hukuman", 2, "Cluster_s")
    plot_data_3b = symbol_wc("pasal_hukuman", 3, "Cluster_s")
    plot_data_4b = symbol_wc("pasal_hukuman", 4, "Cluster_s")
    plot_data_5b = symbol_wc("pasal_hukuman", 5, "Cluster_s")
    plot_data_6b = symbol_wc("pasal_hukuman", 6, "Cluster_s")
    plot_data_7b = symbol_wc("pasal_hukuman", 7, "Cluster_s")
    plot_data_8b = symbol_wc("pasal_hukuman", 8, "Cluster_s")
    
    plot_data_0c = vehicle_wc("jenis_kendaraan", 0)
    plot_data_1c = vehicle_wc("jenis_kendaraan", 1)
    plot_data_2c = vehicle_wc("jenis_kendaraan", 2)
    plot_data_3c = vehicle_wc("jenis_kendaraan", 3)
    plot_data_4c = vehicle_wc("jenis_kendaraan", 4)
    plot_data_5c = vehicle_wc("jenis_kendaraan", 5)
    plot_data_6c = vehicle_wc("jenis_kendaraan", 6)
    plot_data_7c = vehicle_wc("jenis_kendaraan", 7)
    plot_data_8c = vehicle_wc("jenis_kendaraan", 8)



    return render_template('home/word-cloud.html', segment='word-cloud',
    plot_cluster0a=plot_data_0a, 
    plot_cluster1a=plot_data_1a,
    plot_cluster2a=plot_data_2a,
    plot_cluster3a=plot_data_3a,
    plot_cluster4a=plot_data_4a,
    plot_cluster5a=plot_data_5a,
    plot_cluster6a=plot_data_6a,
    plot_cluster7a=plot_data_7a,
    plot_cluster8a=plot_data_8a,

    plot_cluster0b=plot_data_0b,
    plot_cluster1b=plot_data_1b,
    plot_cluster2b=plot_data_2b,
    plot_cluster3b=plot_data_3b,
    plot_cluster4b=plot_data_4b,
    plot_cluster5b=plot_data_5b,
    plot_cluster6b=plot_data_6b,
    plot_cluster7b=plot_data_7b,
    plot_cluster8b=plot_data_8b,

    plot_cluster0c=plot_data_0c,
    plot_cluster1c=plot_data_1c,
    plot_cluster2c=plot_data_2c,
    plot_cluster3c=plot_data_3c,
    plot_cluster4c=plot_data_4c,
    plot_cluster5c=plot_data_5c,
    plot_cluster6c=plot_data_6c,
    plot_cluster7c=plot_data_7c,
    plot_cluster8c=plot_data_8c
    )


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

@blueprint.route('/word-clouds.html')
@login_required
def gfg():

    return render_template('home/word-clouds.html')

@blueprint.route('/form-wc.html', methods=['GET','POST'])
@login_required
def wcs():
    if request.method == 'POST':
        columns = request.form.get('column')
        clusters = request.form.get('cluster')
        tables = request.form.get('table')
        details_t = ["Pasal 106 ayat (5) huruf a = Pada saat diadakan pemeriksaan Kendaraan Bermotor di Jalan setiap orang yang mengemudikan Kendaraan Bermotor wajib menunjukkan Surat Tanda Nomor Kendaraan Bermotor atau Surat Tanda Coba Kendaraan Bermotor.", "Pasal 106 ayat (5) huruf b = Pada saat diadakan pemeriksaan Kendaraan Bermotor di Jalan setiap orang yang mengemudikan Kendaraan Bermotor wajib menunjukkan Surat Izin Mengemudi (SIM).", "Pasal 77 ayat (1) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib memiliki Surat Izin Mengemudi sesuai dengan jenis Kendaraan Bermotor yang dikemudikan.", "Pasal 106 ayat (4) huruf c = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan Alat Pemberi Isyarat Lalu Lintas.", "Pasal 68 ayat (1) = Setiap Kendaraan Bermotor yang dioperasikan di Jalan wajib dilengkapi dengan Surat Tanda Nomor Kendaraan Bermotor dan Tanda Nomor Kendaraan Bermotor.", "Pasal 106 ayat (4) huruf a =  Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan rambu perintah atau rambu larangan dan Pasal 106 ayat (4) huruf b =  Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan Marka Jalan. ", "Pasal 106 ayat (6) = Setiap orang yang mengemudikan Kendaraan Bermotor beroda empat atau lebih di Jalan dan penumpang yang duduk di sampingnya wajib mengenakan sabuk keselamatan. ", "Pasal 106 ayat (8) = Setiap orang yang mengemudikan Sepeda Motor dan Penumpang Sepeda Motor wajib mengenakan helm yang memenuhi standar nasional Indonesia.", "Pasal 106 ayat (3) =Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan wajib mematuhi ketentuan tentang persyaratan teknis dan laik jalan dan Pasal 106 ayat (5) huruf c = Pada saat diadakan pemeriksaan Kendaraan Bermotor di Jalan setiap orang yang mengemudikan Kendaraan Bermotor wajib menunjukkan bukti lulus uji berkala "]
        details_h = ["Pasal 288 ayat (1) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak dilengkapi dengan Surat Tanda Nomor Kendaraan Bermotor atau Surat Tanda Coba Kendaraan Bermotor yang ditetapkan oleh Kepolisian Negara Republik Indonesia sebagaimana dimaksud dalam Pasal 106 ayat (5) huruf a dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 288 ayat (2) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak dapat menunjukkan Surat Izin Mengemudi yang sah sebagaimana dimaksud dalam Pasal 106 ayat (5) huruf b dipidana dengan pidana kurungan paling lama 1 (satu) bulan dan/atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah).", "Pasal 281 = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak memiliki Surat Izin Mengemudi sebagaimana dimaksud dalam Pasal 77 ayat (1) dipidana dengan pidana kurungan paling lama 4 (empat) bulan atau denda paling banyak Rp1.000.000,00 (satu juta rupiah).", "Pasal 287 ayat (2) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang melanggar aturan perintah atau larangan yang dinyatakan dengan Alat Pemberi Isyarat Lalu Lintas sebagaimana dimaksud dalam Pasal 106 ayat (4) huruf c dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 280 = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang tidak dipasangi Tanda Nomor Kendaraan Bermotor yang ditetapkan oleh Kepolisian Negara Republik Indonesia sebagaimana dimaksud dalam Pasal 68 ayat (1) dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 287 ayat (1) = Setiap orang yang mengemudikan Kendaraan Bermotor di Jalan yang melanggar aturan perintah atau larangan yang dinyatakan dengan Rambu Lalu Lintas sebagaimana dimaksud dalam Pasal 106 ayat (4) huruf a atau Marka Jalan sebagaimana dimaksud dalam Pasal 106 ayat (4) huruf b dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah).", "Pasal 289 = Setiap orang yang mengemudikan Kendaraan Bermotor atau Penumpang yang duduk di samping Pengemudi yang tidak mengenakan sabuk keselamatan sebagaimana dimaksud dalam Pasal 106 ayat (6) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah).", "Pasal 291 ayat (1) = Setiap orang yang mengemudikan Sepeda Motor tidak mengenakan helm standar nasional Indonesia sebagaimana dimaksud dalam Pasal 106 ayat (8) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah) dan Pasal 291 ayat (2) = Setiap orang yang mengemudikan Sepeda Motor yang membiarkan penumpangnya tidak mengenakan helm sebagaimana dimaksud dalam Pasal 106 ayat (8) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah).", "Pasal 285 ayat (1) = Setiap orang yang mengemudikan Sepeda Motor di Jalan yang tidak memenuhi persyaratan teknis dan laik jalan yang meliputi kaca spion, klakson, lampu utama, lampu rem, lampu penunjuk arah, alat pemantul cahaya, alat pengukur kecepatan, knalpot, dan kedalaman alur ban sebagaimana dimaksud dalam Pasal 106 ayat (3) juncto Pasal 48 ayat (2) dan ayat (3) dipidana dengan pidana kurungan paling lama 1 (satu) bulan atau denda paling banyak Rp250.000,00 (dua ratus lima puluh ribu rupiah) dan Pasal 288 ayat (3) = Setiap orang yang mengemudikan mobil penumpang umum, mobil bus, mobil barang, kereta gandengan, dan kereta tempelan yang tidak dilengkapi dengan surat keterangan uji berkala dan tanda lulus uji berkala sebagaimana dimaksud dalam Pasal 106 ayat (5) huruf c dipidana dengan pidana kurungan paling lama 2 (dua) bulan atau denda paling banyak Rp500.000,00 (lima ratus ribu rupiah)."]

        # condition for input
        if tables == 'Cluster_s':
            result = symbol_wc(columns, clusters, tables)
        elif tables == 'Cluster_a':
            result = grouped_wc(columns, clusters, tables)
        elif columns == 'jenis_kendaraan':
            result = vehicle_wc(columns, clusters)
        
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
                                plot_clusters = clusters, plot_tables = tables, segment="form")


    return render_template('home/form.html', plot_forms, plot_details, segment="form")
