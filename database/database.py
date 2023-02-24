from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker
from utils          import getConfig

''' Create engine and session communicate with database '''
engine  = create_engine('postgresql://' + getConfig('user') + ':' + getConfig('password') + '@localhost/' + getConfig('database') + '', echo=True)
Session = sessionmaker(bind=engine)

from entity.model        import Models,  Base
from entity.user          import Users,   Base
from entity.classes       import Classes, Base
from entity.images        import Images,  Base
from entity.trained_model import TrainedModel, Base
from entity.prediction    import Predictions,  Base
from entity.trained_on    import TrainedOn,    Base

''' Create all table'''
Base.metadata.create_all(engine)