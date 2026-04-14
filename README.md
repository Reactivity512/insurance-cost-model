# 🏥 Прогнозирование стоимости медицинской страховки

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/downloads/)
[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Live%20Demo-yellow)](https://huggingface.co/spaces/SergeyR256/insurance-cost-model)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg)](https://www.docker.com/)

ML-модель для прогнозирования индивидуальных медицинских расходов на основе демографических данных и образа жизни. Проект демонстрирует полный цикл: от разведочного анализа данных (EDA) до развертывания REST API в Docker-контейнере.

**Попробуйте онлайн:** [🤗 Hugging Face Space](https://huggingface.co/spaces/SergeyR256/insurance-cost-model)

## 📊 Источник данных

Модель обучена на датасете **Medical Cost Personal Datasets** [(Kaggle)](https://www.kaggle.com/datasets/mirichoi0218/insurance).

> Miri Choi. (2018). *Medical Cost Personal Datasets*. Kaggle.  
> Лицензия: [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)

### Поля датасета:
| Колонка | Описание |
|---------|----------|
| `age` | Возраст основного бенефициара |
| `sex` | Пол |
| `bmi` | Индекс массы тела |
| `children` | Количество детей, покрытых страховкой |
| `smoker` | Статус курения |
| `region` | Регион проживания в США |
| `charges` | Индивидуальные медицинские расходы (целевая переменная) |

## 📊 Метрики модели

| Метрика | Значение |
|---------|----------|
| **MAE** (Средняя абсолютная ошибка) | `$4,193` |
| **RMSE** (Корень из среднеквадратичной ошибки) | `$5,800` |
| **R² Score** (Коэффициент детерминации) | `0.7833` |

> Модель объясняет **~78%** дисперсии стоимости страховки. Использован `QuantileTransformer` для борьбы с выбросами в целевой переменной и `Ridge` регрессия для предотвращения переобучения.

## 📁 Структура проекта
```
insurance-cost-predictor/
│
├── .gitignore                 # Исключения для Git
├── README.md                  # Документация проекта
├── requirements.txt           # Python-зависимости
├── Dockerfile                 # Инструкция сборки Docker-образа
├── main.py                    # FastAPI сервер
├── insurance_model_pipeline.joblib   # Сериализованный пайплайн (препроцессинг + модель)
└── notebooks/
    └── 01_eda_and_training.ipynb     # EDA и обучение модели
```

## 🔧 Признаки

Модель принимает на вход следующие параметры клиента:
- `age` (int) — Возраст
- `sex` (str) — Пол (`male` / `female`)
- `bmi` (float) — Индекс массы тела
- `children` (int) — Количество детей
- `smoker` (str) — Курит ли (`yes` / `no`)
- `region` (str) — Регион США (`southwest`, `southeast`, `northwest`, `northeast`)

## 🚀 Демо

Попробуйте модель онлайн без установки:  
👉 **[Student Performance Predictor на Hugging Face](https://huggingface.co/spaces/SergeyR256/insurance-cost-model)**

## 🚀 Быстрый старт (Docker)

Самый простой способ запустить API — использовать Docker.

### 1. Сборка образа
```bash
docker build -t insurance-api .
```

### 2. Запуск контейнера
```bash
docker run -p 8000:8000 insurance-api
```

Сервер будет доступен по адресу: http://127.0.0.1:8000

### 3. Документация API

Перейдите по ссылке для интерактивного тестирования через Swagger UI:

* **Swagger UI**: http://127.0.0.1:8000/docs
* **ReDoc**: http://127.0.0.1:8000/redoc

### 📮 Пример запроса

cURL (Linux/Mac):
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "age": 19,
           "sex": "female",
           "bmi": 27.9,
           "children": 0,
           "smoker": "yes",
           "region": "southwest"
         }'
```

PowerShell (Windows)
```powershell
irm -Uri "http://127.0.0.1:8000/predict" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"age":19,"sex":"female","bmi":27.9,"children":0,"smoker":"yes","region":"southwest"}'
```

Пример ответа
```json
{
  "predicted_charges_usd": 21984.47,
  "input_data": {
    "age": 19,
    "sex": "female",
    "bmi": 27.9,
    "children": 0,
    "smoker": "yes",
    "region": "southwest"
  }
}
```

### 🧪 Локальный запуск (без Docker)

```bash
# 1. Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate для Windows

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Запустите сервер
uvicorn main:app --reload
```

## Эксперименты и выводы

В процессе работы над моделью были протестированы различные подходы:

* Базовая `LinearRegression` (R² ~ 0.60)
* `Ridge` регуляризация
* Логарифмирование целевой переменной
* Финальное решение: QuantileTransformer + Ridge

Ключевой инсайт: `QuantileTransformer` позволил справиться с экстремальными выбросами (клиенты со стоимостью страховки > $50,000), подняв R² с 0.61 до 0.78 без добавления новых признаков.

Детали исследования доступны в ноутбуке `notebooks/01_eda_and_training.ipynb`.

## 🛠 Технологии

* Python 3.14
* Scikit-learn — препроцессинг, обучение, пайплайн
* FastAPI — REST API
* Uvicorn — ASGI сервер
* Docker — контейнеризация
* Pandas, NumPy, Matplotlib, Seaborn — анализ данных

## 📄 Лицензия

* MIT

## 👤 Автор

Reactivity512