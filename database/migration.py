from database import engine


from entity._model        import Models,  Base
from entity.user          import Users,   Base
from entity.classes       import Classes, Base
from entity.images        import Images,  Base
from entity.trained_model import TrainedModel, Base
from entity.prediction    import Predictions,  Base
from entity.trained_on    import TrainedOn,    Base

''' Create all table'''
Base.metadata.create_all(engine)
