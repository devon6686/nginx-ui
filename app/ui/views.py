from app.ui import ui
import flask
import os


@ui.route('/',  methods=['GET'])
def index():
    """
    Delivers the home page of Nginx UI.

    :return: Rendered HTML document.
    :rtype: str
    """
    nginx_path = flask.current_app.config['MAIN_CONFIG_PATH']
    #config = [f for f in os.listdir(nginx_path) if os.path.isfile(os.path.join(nginx_path, f))]
    config = [f for f in os.listdir(nginx_path) if f == "nginx.conf" ]
    return flask.render_template('index.html', config=config)
