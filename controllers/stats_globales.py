import hug

from database.entity import Predictions
from database.database import session

@hug.get('/total_pred')
def recup_stats_globales():
    totalPred    = session.query(Predictions).count() # Nb total de prédictions
    mauvaisePred = session.query(Predictions.id).where(Predictions.classe_id == None ).count() # Nb de mauvaises preds
    return {'total_predictions': totalPred, 'mauvaises_predictions': mauvaisePred}
