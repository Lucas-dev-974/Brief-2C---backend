import hug

from database.entity import Predictions
from database.database import session

@hug.get('/total_pred')
def recup_stats_globales():
    totalPred = session.query(Predictions).count()
    return {'total_predictions': totalPred}
