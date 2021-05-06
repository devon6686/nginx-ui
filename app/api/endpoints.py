import datetime
import io
import os
import flask
import subprocess

from app.api import api


@api.route('/config/<name>',  methods=['GET'])
def get_config(name: str):
    """
    Reads the file with the corresponding name that was passed.

    :param name: Configuration file name
    :type name: str

    :return: Rendered HTML document with content of the configuration file.
    :rtype: str
    """
    nginx_path = flask.current_app.config['MAIN_CONFIG_PATH']

    with io.open(os.path.join(nginx_path, name), 'r') as f:
        _file = f.read()

    return flask.render_template('config.html', name=name, file=_file), 200


@api.route('/config/<name>', methods=['POST'])
def post_config(name: str):
    """
    Accepts the customized configuration and saves it in the configuration file with the supplied name.

    :param name: Configuration file name
    :type name: str

    :return:
    :rtype: werkzeug.wrappers.Response
    """
    content = flask.request.get_json()
    nginx_path = flask.current_app.config['MAIN_CONFIG_PATH']

    with io.open(os.path.join(nginx_path, name), 'w') as f:
        f.write(content['file'])

    return flask.make_response({'success': True}), 200


@api.route('/env/config/<env>',  methods=['GET'])
def get_env_config(env: str):
    """
    Reads the file with the corresponding name that was passed.

    :param env: Configuration file name
    :type env: str

    :return: Rendered HTML document with content of the configuration file.
    :rtype: str
    """
    nginx_path = flask.current_app.config['NGINX_PATH']
    main_config_dir = flask.current_app.config['MAIN_CONFIG_DIR']
    main_config_name = flask.current_app.config['MAIN_CONFIG_NAME']
    main_config_path = os.path.join(nginx_path, env, main_config_dir, main_config_name)
    with io.open(main_config_path, 'r') as f:
        _file = f.read()

    return flask.render_template('config.html', env=env, name=main_config_name, file=_file), 200


@api.route('/env/config/<name>', methods=['POST'])
def post_env_config(name: str):
    """
    Accepts the customized configuration and saves it in the configuration file with the supplied name.

    :param name: Configuration file name
    :type name: str

    :return:
    :rtype: werkzeug.wrappers.Response
    """
    content = flask.request.get_json()
    nginx_path = flask.current_app.config['NGINX_PATH']
    main_config_dir = flask.current_app.config['MAIN_CONFIG_DIR']
    # main_config_name = flask.current_app.config['MAIN_CONFIG_NAME']
    env, filename = name.split('-', maxsplit=1)
    main_config_path = os.path.join(nginx_path, env, main_config_dir, filename)
    with io.open(main_config_path, 'w') as f:
        f.write(content['file'])

    return flask.make_response({'success': True}), 200


@api.route('/sync/<env>', methods=['POST'])
def sync_conf(env: str):
    """
    sync domain config to correspond nginx host
    :param env: environment name
    :type env: str
    """
    nginx_host = flask.current_app.config['NGINX_HOST_MAP'].get(env)
    local_env_dir = os.path.join(flask.current_app.config['NGINX_PATH'], env,
                                 flask.current_app.config['DOMAIN_CONFIG_DIR'])
    remote_domain_dir = flask.current_app.config['REMOTE_NGINX_DOMAIN_DIR']
    sync_cmd = f"scp {local_env_dir}/*.conf stops@{nginx_host}:{remote_domain_dir}"
    # print(sync_cmd)
    ret = subprocess.run(sync_cmd, shell=True, stderr=subprocess.PIPE)
    if ret.returncode == 0:
        subprocess.run(sync_cmd, shell=True)
        flask.jsonify({'success': True}), 200
    else:
        flask.jsonify({'success': False}), 400


@api.route('/reload/<env>', methods=['POST'])
def reload_nginx(env: str):
    """
    :param env: environment name
    :type env: str
    """
    nginx_sbin_path = flask.current_app.config['NGINX_SBIN']
    nginx_sbin = os.path.join(nginx_sbin_path, 'nginx')
    nginx_host = flask.current_app.config['NGINX_HOST_MAP'].get(env)
    check_cmd = f"ssh stops@{nginx_host} 'sudo {nginx_sbin} -t'"
    reload_cmd = f"ssh stops@{nginx_host} 'sudo {nginx_sbin} -s reload'"
    # ret = subprocess.run(check_cmd, shell=True, capture_output=True) //3.6+版本支持
    print(nginx_host, check_cmd)
    #  3.6版本不支持capture_output
    ret = subprocess.run(check_cmd, shell=True, stderr=subprocess.PIPE)

    if ret.returncode == 0:
        subprocess.run(reload_cmd, shell=True)
        flask.jsonify({'success': True}), 200
    else:
        flask.jsonify({'success': False}), 400


@api.route('/domains', methods=['GET'])
def get_domains():
    """
    Reads all files from the configuration file directory and checks the state of the site configuration.

    :return: Rendered HTML document with the domains
    :rtype: str
    """
    config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    sites_available = []
    sites_enabled = []

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            domain, state = _.rsplit('.', 1)

            if state == 'conf':
                time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(config_path, _)))

                sites_available.append({
                    'name': domain,
                    'time': time
                })
                sites_enabled.append(domain)
            elif state == 'disabled':
                time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(config_path, _)))

                sites_available.append({
                    'name': domain.rsplit('.', 1)[0],
                    'time': time
                })

    # sort sites by name
    sites_available = sorted(sites_available, key=lambda _: _['name'])
    return flask.render_template('domains.html', sites_available=sites_available, sites_enabled=sites_enabled), 200


@api.route('/env/domains/<env>', methods=['GET'])
def get_env_domains(env: str):
    """
    Reads all files from the configuration file directory and checks the state of the site configuration.

    :return: Rendered HTML document with the domains
    :rtype: str
    """
    nginx_path = flask.current_app.config['NGINX_PATH']
    domain_dir = flask.current_app.config['DOMAIN_CONFIG_DIR']
    config_path = os.path.join(nginx_path, env, domain_dir)
    sites_available = []
    sites_enabled = []

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            domain, state = _.rsplit('.', 1)

            if state == 'conf':
                time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(config_path, _)))

                sites_available.append({
                    'name': domain,
                    'time': time
                })
                sites_enabled.append(domain)
            elif state == 'disabled':
                time = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(config_path, _)))

                sites_available.append({
                    'name': domain.rsplit('.', 1)[0],
                    'time': time
                })

    # sort sites by name
    sites_available = sorted(sites_available, key=lambda _: _['name'])
    return flask.render_template('domains.html', env=env, sites_available=sites_available, sites_enabled=sites_enabled), 200


@api.route('/domain/<name>', methods=['GET'])
def get_domain(name: str):
    """
    Takes the name of the domain configuration file and
    returns a rendered HTML with the current configuration of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Rendered HTML document with the domain
    :rtype: str
    """
    config_path = flask.current_app.config['NGINX_PATH']
    _file = ''
    enabled = True

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                domain, state = _.rsplit('.', 1)

                if state == 'disabled':
                    enabled = False

                with io.open(os.path.join(config_path, _), 'r') as f:
                    _file = f.read()

                break

    return flask.render_template('domain.html', name=name, file=_file, enabled=enabled), 200


@api.route('/domain/<name>', methods=['POST'])
def post_domain(name: str):
    """
    Creates the configuration file of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    new_domain = flask.render_template('new_domain.j2', name=name)
    name = name + '.conf.disabled'

    try:
        with io.open(os.path.join(config_path, name), 'w') as f:
            f.write(new_domain)

        response = flask.jsonify({'success': True}), 201
    except Exception as ex:
        response = flask.jsonify({'success': False, 'error_msg': ex}), 500

    return response


@api.route('/domain/<name>', methods=['DELETE'])
def delete_domain(name: str):
    """
    Deletes the configuration file of the corresponding domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    removed = False

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                remove_app_path = os.path.join(config_path, _)
                os.rename(remove_app_path, remove_app_path + ".bak")
                removed = not os.path.exists(remove_app_path)
                break
    if removed:
        return flask.jsonify({'success': True}), 200
    else:
        return flask.jsonify({'success': False}), 400


@api.route('/domain/<name>', methods=['PUT'])
def put_domain(name: str):
    """
    Updates the configuration file with the corresponding domain name.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    content = flask.request.get_json()
    config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                with io.open(os.path.join(config_path, _), 'w') as f:
                    f.write(content['file'])

    return flask.make_response({'success': True}), 200


@api.route('/domain/<name>/enable', methods=['POST'])
def enable_domain(name: str):
    """
    Activates the domain in Nginx so that the configuration is applied.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    content = flask.request.get_json()
    config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(name):
                if content['enable']:
                    new_filename, disable = _.rsplit('.', 1)
                    os.rename(os.path.join(config_path, _), os.path.join(config_path, new_filename))
                else:
                    os.rename(os.path.join(config_path, _), os.path.join(config_path, _ + '.disabled'))

    return flask.make_response({'success': True}), 200


@api.route('/env/domain/<name>', methods=['GET'])
def get_env_domain(name: str):
    """
    Takes the name of the domain configuration file and
    returns a rendered HTML with the current configuration of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Rendered HTML document with the domain
    :rtype: str
    """
    nginx_path = flask.current_app.config['NGINX_PATH']
    domain_dir = flask.current_app.config['DOMAIN_CONFIG_DIR']
    env, filename = name.split('-')
    config_path = os.path.join(nginx_path, env, domain_dir)
    _file = ''
    enabled = True

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(filename):
                domain, state = _.rsplit('.', 1)

                if state == 'disabled':
                    enabled = False

                with io.open(os.path.join(config_path, _), 'r') as f:
                    _file = f.read()

                break

    return flask.render_template('domain.html', name=filename, file=_file, enabled=enabled), 200


@api.route('/env/domain/<name>', methods=['POST'])
def post_env_domain(name: str):
    """
    Creates the configuration file of the domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    # config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    nginx_path = flask.current_app.config['NGINX_PATH']
    domain_dir = flask.current_app.config['DOMAIN_CONFIG_DIR']
    env, filename = name.split('-')
    config_path = os.path.join(nginx_path, env, domain_dir)

    new_domain = flask.render_template('new_domain.j2', name=filename)
    filename = filename + '.conf.disabled'

    try:
        with io.open(os.path.join(config_path, filename), 'w') as f:
            f.write(new_domain)

        response = flask.jsonify({'success': True}), 201
    except Exception as ex:
        response = flask.jsonify({'success': False, 'error_msg': ex}), 500

    return response


@api.route('/env/domain/<name>', methods=['DELETE'])
def delete_env_domain(name: str):
    """
    Deletes the configuration file of the corresponding domain.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    # config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    nginx_path = flask.current_app.config['NGINX_PATH']
    domain_dir = flask.current_app.config['DOMAIN_CONFIG_DIR']
    env, filename = name.split('-', maxsplit=1)
    config_path = os.path.join(nginx_path, env, domain_dir)
    removed = False

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(filename):
                remove_app_path = os.path.join(config_path, _)
                os.rename(remove_app_path, remove_app_path + ".bak")
                removed = not os.path.exists(remove_app_path)
                break
    if removed:
        return flask.jsonify({'success': True}), 200
    else:
        return flask.jsonify({'success': False}), 400


@api.route('/env/domain/<name>', methods=['PUT'])
def put_env_domain(name: str):
    """
    Updates the configuration file with the corresponding domain name.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    content = flask.request.get_json()
    # config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    nginx_path = flask.current_app.config['NGINX_PATH']
    domain_dir = flask.current_app.config['DOMAIN_CONFIG_DIR']
    env, filename = name.split('-', maxsplit=1)
    config_path = os.path.join(nginx_path, env, domain_dir)

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(filename):
                with io.open(os.path.join(config_path, _), 'w') as f:
                    f.write(content['file'])

    return flask.make_response({'success': True}), 200


@api.route('/env/domain/<name>/enable', methods=['POST'])
def enable_env_domain(name: str):
    """
    Activates the domain in Nginx so that the configuration is applied.

    :param name: The domain name that corresponds to the name of the file.
    :type name: str

    :return: Returns a status about the success or failure of the action.
    """
    content = flask.request.get_json()
    # config_path = flask.current_app.config['DOMAIN_CONFIG_PATH']
    nginx_path = flask.current_app.config['NGINX_PATH']
    domain_dir = flask.current_app.config['DOMAIN_CONFIG_DIR']
    env, filename = name.split('-', maxsplit=1)
    config_path = os.path.join(nginx_path, env, domain_dir)

    for _ in os.listdir(config_path):

        if os.path.isfile(os.path.join(config_path, _)):
            if _.startswith(filename):
                if content['enable']:
                    new_filename, disable = _.rsplit('.', 1)
                    os.rename(os.path.join(config_path, _), os.path.join(config_path, new_filename))
                else:
                    os.rename(os.path.join(config_path, _), os.path.join(config_path, _ + '.disabled'))

    return flask.make_response({'success': True}), 200

