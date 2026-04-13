from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import logging

logging.basicConfig(filename='predictions.log', level=logging.INFO)

# 1. Загружаем модель при старте сервера
model = joblib.load('insurance_model_pipeline.joblib')

# 2. Описываем, какие данные ждем
class ClientData(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str

app = FastAPI(title="Insurance Cost Predictor")

@app.post("/predict")
async def predict(data: ClientData):
    # Превращаем JSON в DataFrame
    input_df = pd.DataFrame([data.dict()])
    
    # Делаем предсказание
    prediction = model.predict(input_df)[0]

    logging.info(f"Input: {data.dict()}, Predicted: {prediction}")
    
    return {
        "predicted_charges_usd": round(prediction, 2),
        "input_data": data
    }

@app.get("/health")
async def health():
    return {"status": "ok"}