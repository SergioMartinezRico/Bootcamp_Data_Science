import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics


df = pd.read_csv("./data/USA_Housing.csv")
X = df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']]
y = df["Price"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state = 11)

#shapes del df y los conjuntos de entrenamiento y prueba
print(X.shape)
print(X_train.shape)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

#entrenamiento 
lm = LinearRegression()
lm.fit(X_train, y_train)
pred = lm.predict(X_test)

#metricas
print("MAE: ", metrics.mean_absolute_error(y_test, pred))
