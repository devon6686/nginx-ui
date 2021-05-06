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
    # nginx_path = flask.current_app.config['MAIN_CONFIG_PATH']
    # config = [f for f in os.listdir(nginx_path) if f == "nginx.conf"]
    config = flask.current_app.config['MAIN_CONFIG_NAME']
    environments = flask.current_app.config['ENV_LIST']
    return flask.render_template('index.html', config=config, envs=environments)
