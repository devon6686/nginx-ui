import os


class Config(object):
    SECRET_KEY = os.urandom(64).hex()

    NGINX_PATH = '/usr/local/stapply/nginx/'
    NGINX_SBIN = os.path.join(NGINX_PATH, 'sbin')
    MAIN_CONFIG_PATH = os.path.join(NGINX_PATH, 'conf')
    DOMAIN_CONFIG_PATH = os.path.join(NGINX_PATH, 'conf.d')
    ENV_LIST = ['dev', 'test', 'pre', 'prod']

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


class WorkingConfig(Config):
    DEBUG = True


config = {
    'dev': DevConfig,
    'default': WorkingConfig
}
