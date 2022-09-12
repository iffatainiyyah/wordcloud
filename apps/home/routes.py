# -*- encoding: utf-8 -*-


from apps.home.visualization import word_cloud, word_clouds
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
    # word_cloud(cluster ke berapa, nama tabelnya)
    # word cloud singkatan
    plot_data_0a = word_cloud("pasal_tuntutan", 0, "Cluster_s")
    plot_data_1a = word_cloud("pasal_tuntutan", 1, "Cluster_s")
    plot_data_2a = word_cloud("pasal_tuntutan", 2, "Cluster_s")
    plot_data_3a = word_cloud("pasal_tuntutan", 3, "Cluster_s")
    plot_data_4a = word_cloud("pasal_tuntutan", 4, "Cluster_s")
    plot_data_5a = word_cloud("pasal_tuntutan", 5, "Cluster_s")
    plot_data_6a = word_cloud("pasal_tuntutan", 6, "Cluster_s")
    plot_data_7a = word_cloud("pasal_tuntutan", 7, "Cluster_s")
    plot_data_8a = word_cloud("pasal_tuntutan", 8, "Cluster_s")

    plot_data_0b = word_cloud("pasal_hukuman", 0, "Cluster_s")
    plot_data_1b = word_cloud("pasal_hukuman", 1, "Cluster_s")
    plot_data_2b = word_cloud("pasal_hukuman", 2, "Cluster_s")
    plot_data_3b = word_cloud("pasal_hukuman", 3, "Cluster_s")
    plot_data_4b = word_cloud("pasal_hukuman", 4, "Cluster_s")
    plot_data_5b = word_cloud("pasal_hukuman", 5, "Cluster_s")
    plot_data_6b = word_cloud("pasal_hukuman", 6, "Cluster_s")
    plot_data_7b = word_cloud("pasal_hukuman", 7, "Cluster_s")
    plot_data_8b = word_cloud("pasal_hukuman", 8, "Cluster_s")
    
    plot_data_0c = word_clouds("jenis_kendaraan", 0, "Cluster_s")
    plot_data_1c = word_clouds("jenis_kendaraan", 1, "Cluster_s")
    plot_data_2c = word_clouds("jenis_kendaraan", 2, "Cluster_s")
    plot_data_3c = word_clouds("jenis_kendaraan", 3, "Cluster_s")
    plot_data_4c = word_clouds("jenis_kendaraan", 4, "Cluster_s")
    plot_data_5c = word_clouds("jenis_kendaraan", 5, "Cluster_s")
    plot_data_6c = word_clouds("jenis_kendaraan", 6, "Cluster_s")
    plot_data_7c = word_clouds("jenis_kendaraan", 7, "Cluster_s")
    plot_data_8c = word_clouds("jenis_kendaraan", 8, "Cluster_s")


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
    plot_cluster8c=plot_data_8c,
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


