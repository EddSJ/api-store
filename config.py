from distutils.command.config import config


class DevelopmentConfig:
    """
    Development configuration
    """
    DEBUG = True
    MYSQL_HOST = 'remotemysql.com'
    MYSQL_USER = 'FVJpgw76FR'
    MYSQL_PASSWORD = '0uDPWv3khs'
    MYSQL_DB = 'FVJpgw76FR'

config = {
    'development': DevelopmentConfig
}
