import os


class Config(object):
    SECRET_KEY = os.urandom(64).hex()

    # NGINX_PATH = '/etc/nginx'
    NGINX_PATH = '/Users/devon/Desktop/project/python/nginx-ui/nginx'
    NGINX_SBIN = '/usr/local/ng/nginx/sbin/'
    MAIN_CONFIG_PATH = os.path.join(NGINX_PATH, 'conf')
    # DOMAIN_CONFIG_PATH = os.path.join(NGINX_PATH, 'conf.d')
    MAIN_CONFIG_DIR = 'conf'
    DOMAIN_CONFIG_DIR = 'conf.d'
    MAIN_CONFIG_NAME = 'nginx.conf'
    ENV_LIST = ['dev', 'test', 'pre', 'prod']
    REMOTE_NGINX_DOMAIN_DIR = "/usr/local/ng/nginx/conf.d/"
    NGINX_HOST_MAP = {
        'dev': '10.14.49.198',
        'test': '10.14.49.200',
        'pre': '10.14.49.198',
        'prod': '10.14.49.198'
    }

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
