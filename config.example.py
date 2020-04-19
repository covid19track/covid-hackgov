MODE = "Development"


class Config:
    """Default configuration values for covid_hackgov_server"""
    NODE_NAME = "covid_hackgov_server/Yes"
    SECRET_KEY = "secret-key"
    REGISTRATIONS = False
    DEBUG = False
    IS_SSL = False


class Development(Config):
    """Development configuration values"""
    NODE_NAME = "covid_hackgov_server/DEV"
    SECRET_KEY = "dev-secret-key"
    REGISTRATIONS = False
    DEBUG = True
    IS_SSL = False


class Production(Config):
    """Production configuration values"""
    NODE_NAME = "production_node_name"
    SECRET_KEY = "production-secret-key"
    REGISTRATIONS = True
    IS_SSL = True
