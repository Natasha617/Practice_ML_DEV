from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from data_rec_mod import *
import joblib
import pandas as pd
from catboost import CatBoostClassifier
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

# Загрузка CatBoost
loaded_model = CatBoostClassifier()
loaded_model.load_model('model_catboost', format='cbm')

# Загрузка модели дерево решений
d_tree = joblib.load('d_tree.pkl')
# Загрузка модели Random Forest
random_forest_model = joblib.load('rand_forest.pkl')
# Загрузка модели Logistic Regression
logistic_regression_model = joblib.load('log_reg.pkl')


def predict_catboost(temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue):
    prediction = loaded_model.predict(
        pd.DataFrame([[temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue]],
                     columns=['temperature', 'humidity', 'CO2CosIRValue', 'CO2MG811Value', 'MOX1', 'MOX2', 'MOX3', 'MOX4', 'COValue']))
    return prediction


def predict_logistic_regression_model(temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue):
    prediction = logistic_regression_model.predict(
        pd.DataFrame([[temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue]],
                     columns=['temperature', 'humidity', 'CO2CosIRValue', 'CO2MG811Value', 'MOX1', 'MOX2', 'MOX3', 'MOX4', 'COValue']))
    return prediction


def predict_random_forest_model(temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue):
    prediction = random_forest_model.predict(
        pd.DataFrame([[temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue]],
                     columns=['temperature', 'humidity', 'CO2CosIRValue', 'CO2MG811Value', 'MOX1', 'MOX2', 'MOX3', 'MOX4', 'COValue']))
    return prediction


def predict_tree_model(temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue):
    prediction = d_tree.predict(
        pd.DataFrame([[temperature, humidity, CO2CosIRValue, CO2MG811Value, MOX1, MOX2, MOX3, MOX4, COValue]],
                     columns=['temperature', 'humidity', 'CO2CosIRValue', 'CO2MG811Value', 'MOX1', 'MOX2', 'MOX3', 'MOX4', 'COValue']))
    return prediction



@app.post("/model-predict")
async def ml_predict(inputs: MlRequest):
    try:
        if inputs.choice_model == 'Tree':
            prediction = predict_tree_model(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                            inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3, inputs.MOX4,
                                            inputs.COValue)
        elif inputs.choice_model == 'RandomForest':
            prediction = predict_random_forest_model(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                                     inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3,
                                                     inputs.MOX4, inputs.COValue)
        elif inputs.choice_model == 'LogisticRegression':
            prediction = predict_logistic_regression_model(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                                           inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3,
                                                           inputs.MOX4, inputs.COValue)
        elif inputs.choice_model == 'CatBoost':
            prediction = predict_catboost(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                          inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3, inputs.MOX4,
                                          inputs.COValue)

        response_content = {"prediction": str(prediction[0])}
        return JSONResponse(content=jsonable_encoder(response_content))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/auth')
async  def aut():
    return {'massege': 'ok'}

