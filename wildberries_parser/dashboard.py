import dash
from dash import dcc, html
import plotly.express as px
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# Настройки подключения к БД
DB_NAME = "wildberries"
DB_USER = "postgres"
DB_PASSWORD = "1903"
DB_HOST = "localhost"

# Создаем подключение через SQLAlchemy (рекомендуемый способ)
try:
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
    df = pd.read_sql("SELECT * FROM products", engine)
except Exception as e:
    print(f"Ошибка подключения к базе данных: {e}")
    exit()

# Создаем график
fig = px.bar(df, x="name", y="price", title="Цены на товары Wildberries")

# Создаем и настраиваем Dash приложение
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Аналитика Wildberries", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)  # Исправлено с run_server на run