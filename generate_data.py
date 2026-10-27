import numpy as np
import pandas as pd
from datetime import date
from sqlalchemy import text
from database import get_engine

PRODUCTS = [
    ('Notebook', 'Eletrônicos', 3200, 2450),
    ('Monitor', 'Eletrônicos', 950, 650),
    ('Mouse', 'Acessórios', 85, 42),
    ('Teclado', 'Acessórios', 160, 90),
    ('Cadeira', 'Móveis', 780, 480),
    ('Mesa', 'Móveis', 1100, 720),
    ('Headset', 'Acessórios', 230, 135),
    ('Smartphone', 'Eletrônicos', 2100, 1540),
]
STATES = ['SP', 'RJ', 'MG', 'PR', 'SC', 'RS', 'BA', 'PE']

def main():
    rng = np.random.default_rng(42)
    days = pd.date_range('2025-01-01', '2026-10-26', freq='D')
    rows = []
    for i in range(1, 3001):
        product, category, price, cost = PRODUCTS[int(rng.integers(len(PRODUCTS)))]
        qty = int(rng.integers(1, 5))
        factor = float(rng.uniform(0.9, 1.1))
        rows.append({
            'order_id': f'PED-{i:05d}',
            'order_date': days[int(rng.integers(len(days)))].date(),
            'product': product, 'category': category,
            'state': str(rng.choice(STATES)), 'quantity': qty,
            'unit_price': round(price * factor, 2),
            'unit_cost': round(cost * factor, 2),
        })
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text('TRUNCATE TABLE sales'))
    pd.DataFrame(rows).to_sql('sales', engine, if_exists='append', index=False, method='multi', chunksize=500)
    print('3.000 pedidos fictícios carregados com sucesso.')

if __name__ == '__main__':
    main()
