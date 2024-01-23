from pydantic import BaseModel, validator, root_validator
from typing import Optional
from typing import List, Optional
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Time, CheckConstraint
from sqlalchemy import create_engine, insert, select, update, delete


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

