import funciones as f
import variables as v

df = f.leer(v.path)
f.graficos(df)
X, y  = f.x_y(df, v.target)
X_train, X_test, y_train, y_test = f.test(X, y, v.tamaño_test, v.semilla)
X_train_s, X_test_s = f.escalado(X_train, X_test, v.escalado)
modelo = f.entrenar(X_train_s, y_train, v.layers, v.neuronas_salida, v.epoch, v.batch)