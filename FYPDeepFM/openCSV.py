import pandas as pd
dfTrain = pd.read_csv('data/train.csv')
cols = [c for c in dfTrain.columns if c not in ["FPS", "target"]]

X_train = dfTrain[cols].values
print(X_train)
print(len(X_train[801]))