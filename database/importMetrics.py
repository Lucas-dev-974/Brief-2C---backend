from database import engine
from database import session
from entity.loss import Loss, Base
from entity.accuracy import Accuracy, Base

test_loss = [1.8319686651229858, 0.5200003981590271, 0.4788396656513214, 0.4866270124912262, 0.42248278856277466, 0.42835599184036255, 0.4123890697956085, 0.3884138762950897, 0.366227924823761, 0.3585617244243622]
epoque = len(test_loss)
test_accuracy = [0.6730017066001892, 0.7428731322288513, 0.7836780548095703, 0.7685858011245728, 0.8004471659660339, 0.810508668422699, 0.8116266131401062, 0.8250419497489929, 0.8468418121337891, 0.833985447883606]

val_loss = [0.6471278667449951, 0.6264894008636475, 0.5800009369850159, 0.5650578737258911, 0.5095633268356323, 0.5082858204841614, 0.5054110288619995, 0.5154422521591187, 0.4381738305091858, 0.3915598690509796]
val_accuracy = [0.7272727489471436, 0.7559808492660522, 0.7894737124443054, 0.7464115023612976, 0.8133971095085144, 0.7368420958518982, 0.7464115023612976, 0.7320573925971985, 0.7942583560943604, 0.8564593195915222]

# Test loss
# for i in range(1,epoque+1):

#     newLoss = Loss(epoque = i, value = test_loss[i-1], model_id = 1, validation = False)
#     session.add(newLoss)
#     session.commit()

# Test accuracy
# for i in range(1,epoque+1):

#     newAccuracy = Accuracy(epoque = i, value = test_accuracy[i-1], model_id = 1, validation = False)
#     session.add(newAccuracy)
#     session.commit()

# Val loss
# for i in range(1,epoque+1):

#     newLoss = Loss(epoque = i, value = val_loss[i-1], model_id = 1, validation = True)
#     session.add(newLoss)
#     session.commit()

# Val accuracy
# for i in range(1,epoque+1):

#     newAccuracy = Accuracy(epoque = i, value = val_accuracy[i-1], model_id = 1, validation = True)
#     session.add(newAccuracy)
#     session.commit()