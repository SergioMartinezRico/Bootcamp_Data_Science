import streamlit as st
import funciones as f

st.title("Entrenador de redes neuronales")
# usuarios_win_mac_lin.csv
archivo = st.file_uploader("Subir archivo", type="csv")
target = st.text_input("Introduce la target")
st.write("Parametros de test")
tamaño_test = st.text_input("tamaño del test")

semilla = st.text_input("numero de semilla")
st.write("Tipo de escalado")
escalado = st.text_input("metodo de escalado")
st.write("Opciones de la red neuronal.")
epoch = st.text_input("Epoch:")
batch = st.text_input("Batch:")
nue_salida = st.text_input("Neuronas de salida")


if st.button("Entrenar"):
    df = f.leer(archivo)
    st.write(df)
    X, y  = f.x_y(df, target)
    X_train, X_test, y_train, y_test = f.test(X, y, float(tamaño_test), int(semilla))
    X_train_s, X_test_s = f.escalado(X_train, X_test, escalado)
    history = f.entrenar(X_train_s, y_train, [256,128,64], int(nue_salida), int(epoch), int(batch))
    st.write(history)
    