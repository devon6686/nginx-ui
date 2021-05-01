import os


class Config(object):
    SECRET_KEY = os.urandom(64).hex()

    # NGINX_PATH = '/etc/nginx'
    NGINX_PATH = '/Users/devon/Desktop/project/python/nginx-ui/nginx'
    NGINX_SBIN = '/usr/local/stapply/nginx/sbin/'
    MAIN_CONFIG_PATH = os.path.join(NGINX_PATH, 'conf')
    # DOMAIN_CONFIG_PATH = os.path.join(NGINX_PATH, 'conf.d')
    MAIN_CONFIG_DIR = 'conf'
    DOMAIN_CONFIG_DIR = 'conf.d'
    MAIN_CONFIG_NAME = 'nginx.conf'
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
