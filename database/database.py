from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from utils import getConfig
except:
    from .utils import getConfig
    

''' Create engine and session communicate with database '''
engine  = create_engine('postgresql://' + getConfig('user') + ':' + getConfig('password') + '@localhost/' + getConfig('database') + '', echo=True)
session = sessionmaker(bind=engine)
session = session()
