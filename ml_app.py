import streamlit as st
import pandas as pd
import requests
import json
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
# Set Page Layout
st.set_page_config(layout='wide')

st.title('Авторизация')
login = st.text_input('Логин: ', max_chars=50)
password = password = st.text_input("Введите пароль", type="password")

if st.button('Вход'):
    response_in = requests.get("http://localhost:8000/auth")
    st.success(f'Результат авторизации {response_in.text}')

st.title('Мониторинг безопасности одиноких пожилых людей')
st.header('Введите показатели с датчиков:')

# Создаем список параметров
parameters = ['temperature', 'humidity', 'CO2CosIRValue', 'CO2MG811Value', 'MOX1', 'MOX2', 'MOX3', 'MOX4', 'COValue']

temperature = st.number_input('Температура: ', min_value=0.1, max_value=50.0, value=1.0)
humidity = st.number_input('Влажность : ', min_value=0.1, max_value=100.0, value=1.0)
CO2CosIRValue = st.number_input('уровень CO2CosIR : ', min_value=0.1, max_value=1000.0, value=1.0)
CO2MG811Value = st.number_input('уровень CO2MG811 : ', min_value=0.1, max_value=1000.0, value=1.0)
MOX1 = st.number_input('Значение MOX1 : ', min_value=0.1, max_value=1000.0, value=1.0)
MOX2 = st.number_input('Значение MOX2 : ', min_value=0.1, max_value=1000.0, value=1.0)
MOX3 = st.number_input('Значение MOX3 : ', min_value=0.1, max_value=1000.0, value=1.0)
MOX4 = st.number_input('Значение MOX4 : ', min_value=0.1, max_value=1000.0, value=1.0)
COValue = st.number_input('Уровень CO : ', min_value=0.1, max_value=1500.0, value=1.0)
choice_model = st.selectbox('Выберите модель для предсказания', ['LogisticRegression', 'RandomForest', 'CatBoost', 'Tree'])

data = {
        "temperature": temperature,
        "humidity": humidity,
        "CO2CosIRValue": CO2CosIRValue,
        "CO2MG811Value": CO2MG811Value,
        "MOX1": MOX1,
        "MOX2": MOX2,
        "MOX3": MOX3,
        "MOX4": MOX4,
        "COValue": COValue,
        "choice_model": choice_model
    }
if st.button('Предсказать'):
    response = requests.post("http://localhost:8000/model-predict", data=json.dumps(data))
    st.success(f'Предсказание: {response.text}')

