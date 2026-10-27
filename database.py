import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

load_dotenv()

def get_engine():
    url = os.getenv('DATABASE_URL')
    if not url:
        raise RuntimeError('Configure DATABASE_URL no arquivo .env')
    return create_engine(url, pool_pre_ping=True)

def load_sales():
    query = text('SELECT order_date, order_id, product, category, state, quantity, unit_price, unit_cost FROM sales ORDER BY order_date')
    with get_engine().connect() as connection:
        return pd.read_sql(query, connection, parse_dates=['order_date'])
