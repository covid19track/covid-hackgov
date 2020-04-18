MODE = "Development"

class Config:
    """Default configuration values for covid_hackgov_server"""
    DEBUG = False
    PORT = 3000

class Development(Config):
    """Development configuration values"""
    DEBUG = True

class Production(Config):
    """Production configuration values"""