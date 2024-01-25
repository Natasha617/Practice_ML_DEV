from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from auth.database import User, db
from data_rec_mod import *
import joblib
import pandas as pd
from catboost import CatBoostClassifier
import ssl
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from auth.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jwt import PyJWTError, decode, encode

ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI()

loaded_model = CatBoostClassifier()
loaded_model.load_model('model_catboost', format='cbm')


d_tree = joblib.load('d_tree.pkl')
random_forest_model = joblib.load('rand_forest.pkl')
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


# списание средств
def deduct_money(db: Session, user_id: int, amount: float):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.balance -= amount
        db.commit()
        return True
    return False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Загрузка приватного ключа
with open("auth/jwt-private.pem", "rb") as private_key_file:
    private_key = serialization.load_pem_private_key(
        private_key_file.read(),
        password=None,
        backend=default_backend()
    )

# Загрузка публичного ключа
with open("auth/jwt-public.pem", "rb") as public_key_file:
    public_key = serialization.load_pem_public_key(
        public_key_file.read(),
        backend=default_backend()
    )


# Функция для получения текущего пользователя из JWT токена
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


@app.post("/model-predict")
async def ml_predict(inputs: MlRequest):
    try:
        if inputs.choice_model == 'Tree - 10$':
            prediction = predict_tree_model(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                            inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3, inputs.MOX4,
                                            inputs.COValue)
        elif inputs.choice_model == 'RandomForest - 20$':
            prediction = predict_random_forest_model(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                                     inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3,
                                                     inputs.MOX4, inputs.COValue)
        elif inputs.choice_model == 'LogisticRegression - 10$':
            prediction = predict_logistic_regression_model(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                                           inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3,
                                                           inputs.MOX4, inputs.COValue)
        elif inputs.choice_model == 'CatBoost - 30$':
            prediction = predict_catboost(inputs.temperature, inputs.humidity, inputs.CO2CosIRValue,
                                          inputs.CO2MG811Value, inputs.MOX1, inputs.MOX2, inputs.MOX3, inputs.MOX4,
                                          inputs.COValue)

        response_content = {"prediction": str(prediction[0])}
        return JSONResponse(content=jsonable_encoder(response_content))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post('/auth')
async def authenticate_user(data: PasswordLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == data.login, User.password == data.password).first()
    if user:
        token_data = {"sub": user.login}
        token = jwt.encode(token_data, private_key, algorithm="RS256")
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")


@app.post('/authhh')
async def authenticate_user(data: PasswordLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.login == data.login, User.password == data.password).first()
    if user:
        return {f"Успешно"}
    else:
        return {"Неверные учетные данные"}
