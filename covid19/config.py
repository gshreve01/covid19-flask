import os
basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

def GetURIConfig(username, password):
    return f"postgresql://localhost/Covid19?user={username}&password={password}"

SQLALCHEMY_DATABASE_URI = "postgresql://localhost/Covid19?user=Greg&password=chrisin05"
