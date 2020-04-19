MODE = "Development"


class Config:
    """Default configuration values for covid_hackgov_server"""
    NODE_NAME = "covid_hackgov_server/Yes"
    DEBUG = False
    IS_SSL = False


class Development(Config):
    """Development configuration values"""
    NODE_NAME = "covid_hackgov_server/DEV"
    DEBUG = True
    IS_SSL = False


class Production(Config):
    """Production configuration values"""
    NODE_NAME = "production_node_name"
    IS_SSL = True
