# -*- encoding: utf-8 -*-


from apps.home.visualization import word_cloud
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

@blueprint.route('/word-cloud.html')
@login_required
def index():
    # word_cloud(cluster ke berapa, nama tabelnya)
    # word cloud singkatan
    plot_data_0s = word_cloud(0, "Cluster_s")
    plot_data_1s = word_cloud(1, "Cluster_s")
    plot_data_2s = word_cloud(2, "Cluster_s")
    plot_data_3s = word_cloud(3, "Cluster_s")
    plot_data_4s = word_cloud(4, "Cluster_s")
    plot_data_5s = word_cloud(5, "Cluster_s")
    plot_data_6s = word_cloud(6, "Cluster_s")
    plot_data_7s = word_cloud(7, "Cluster_s")
    plot_data_8s = word_cloud(8, "Cluster_s")

    # word cloud arti
    plot_data_0a = word_cloud(0, "Cluster_a")
    plot_data_1a = word_cloud(1, "Cluster_a")
    plot_data_2a = word_cloud(2, "Cluster_a")
    plot_data_3a = word_cloud(3, "Cluster_a")
    plot_data_4a = word_cloud(4, "Cluster_a")
    plot_data_5a = word_cloud(5, "Cluster_a")
    plot_data_6a = word_cloud(6, "Cluster_a")
    plot_data_7a = word_cloud(7, "Cluster_a")
    plot_data_8a = word_cloud(8, "Cluster_a")


    return render_template('home/word-cloud.html', 
    plot_cluster0s=plot_data_0s, 
    plot_cluster1s=plot_data_1s,
    plot_cluster2s=plot_data_2s,
    plot_cluster3s=plot_data_3s,
    plot_cluster4s=plot_data_4s,
    plot_cluster5s=plot_data_5s,
    plot_cluster6s=plot_data_6s,
    plot_cluster7s=plot_data_7s,
    plot_cluster8s=plot_data_8s,
    plot_cluster0a=plot_data_0a,
    plot_cluster1a=plot_data_1a,
    plot_cluster2a=plot_data_2a,
    plot_cluster3a=plot_data_3a,
    plot_cluster4a=plot_data_4a,
    plot_cluster5a=plot_data_5a,
    plot_cluster6a=plot_data_6a,
    plot_cluster7a=plot_data_7a,
    plot_cluster8a=plot_data_8a,
   
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


