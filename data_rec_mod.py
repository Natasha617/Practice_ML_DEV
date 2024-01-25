from pydantic import BaseModel


class MlRequest(BaseModel):
    temperature: float
    humidity: float
    CO2CosIRValue: float
    CO2MG811Value: float
    MOX1: float
    MOX2: float
    MOX3: float
    MOX4: float
    COValue: float
    choice_model: str


class PasswordLogin(BaseModel):
    login: str
    password: str
