# 🏁 F1 Strategy Predictor
Predicción de las estrategias de carrera en F1 usando Machine Learning.

## Objetivo
El objetivo principal de este proyecto es analizar datos històricos de F1 y constuir un modelo capaz de predecir decisiones estratégicas como las **paradas en boxes**, **tipo de neumático utilizado**, y **eficiencia de las estrategias de carrera**. Está pensado como una aplicación real de **Data Science, Machine Learning y Visualización**, orientada a un entorno competitivo como la F1.

## Tecnologías 
- Python 3
- pandas, NumPy, scikit-learn
- XGBoost / LightGBM
- matplotlib, seaborn, Plotly
- Streamlit (para la demo)
- Jupyter Notebooks

## Intención para las predicciones?

- ¿Parará un piloto en la próxima vuelta?
- ¿Qué tipo de neumático usará en su próxima parada?
- ¿Qué tan eficiente es la estrategia usada comparada con una alternativa?

## Estructura

```bash
f1-strategy-predictor/
├── data/                  # Datasets CSV/JSON
├── notebooks/             # Análisis exploratorio y pruebas
├── src/                   # Scripts de ML
├── app/                   # App interactiva con Streamlit
├── README.md              # Este archivo
└── requirements.txt       # Librerías necesarias
