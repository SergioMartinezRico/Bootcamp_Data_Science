import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow import keras
def leer(path):
    df = pd.read_csv(path)
    return df
def x_y(df, target):
    X = df.drop(columns = [target])
    y = df [target]
    return X, y

def test(X, y, test_size, semilla):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=semilla)
    return X_train, X_test, y_train, y_test

def escalado(X_train, X_test, escalado = None):
    if escalado != None:
        if escalado == "StandarScaler":
            sc = StandardScaler()
            sc.fit(X_train)
            X_train_sc = sc.transform(X_train)
            X_test_sc = sc.transform(X_test)
            return X_train_sc, X_test_sc
        elif escalado == "MinMaxScaler":
            print("minMax")
            mms = MinMaxScaler()
            mms.fit(X_train)
            X_train_mms = mms.transform(X_train)
            X_test_mms = mms.transform(X_test)
            return X_train_mms, X_test_mms
    else:
        return X_train, X_test

def graficos(df):
    plt.figure(figsize=(8,8))
    sns.heatmap(df.corr(numeric_only = True), cmap="coolwarm", vmin = -1, annot= True)
    plt.title("Matriz de coorenacción")

    sns.pairplot(df)
    plt.title("Pairplot")

    plt.show()

def entrenar(X_train_s, y_train, layers_hidden, nue_salida, epoch, batch):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=(X_train_s.shape[1:])))
    for i in layers_hidden:
        model.add(keras.layers.Dense(units = i, activation='relu'))
    
    model.add(keras.layers.Dense(units = nue_salida, activation='softmax'))

    model.compile(
        optimizer = "sgd",
        loss = "sparse_categorical_crossentropy",
        metrics = ["accuracy"]
    )
    model.summary()

    history = model.fit(
        X_train_s,
        y_train,
        batch_size = batch,
        epochs = epoch,
        validation_split = 0.2
    )
    df_history = pd.DataFrame(history.history)
    return df_history