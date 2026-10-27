# SalesScope — Dashboard de Vendas

Projeto de portfólio para Analista de Dados: Python, MySQL, SQL, Pandas, Streamlit e Plotly.

## Funcionalidades
- KPIs: faturamento, lucro bruto estimado, número de pedidos e ticket médio
- Gráficos de faturamento mensal, categoria e estado
- Ranking de produtos, filtros e exportação CSV
- 3.000 pedidos sintéticos reproduzíveis (seed 42)

## Execução local
1. Instale Python 3.11+ e MySQL 8.0+ (MySQL Workbench é opcional).
2. Abra o MySQL Workbench e execute `sql/schema.sql` para criar o banco e a tabela.
3. Confirme que o banco `dashboard_vendas` foi criado.
4. Copie `.env.example` para `.env` e ajuste usuário/senha/host.
5. Crie e ative um ambiente virtual:
   - Windows: `py -m venv .venv` e `.venv\Scripts\activate`
   - Linux/macOS: `python -m venv .venv` e `source .venv/bin/activate`
6. Instale dependências: `pip install -r requirements.txt`.
7. Gere dados: `python generate_data.py`.
8. Inicie: `streamlit run app.py`.

**Atenção:** `generate_data.py` usa TRUNCATE e substitui os dados existentes da tabela `sales`. Use apenas em banco de demonstração.

## Definições dos indicadores
- Faturamento = SUM(quantity * unit_price)
- Lucro bruto estimado = SUM(quantity * (unit_price - unit_cost))
- Pedidos = COUNT(DISTINCT order_id)
- Ticket médio = faturamento / pedidos

## SQL de exemplo
```sql
SELECT category, ROUND(SUM(quantity * unit_price), 2) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;
```

## Publicação
Publique o repositório no GitHub sem o `.env`. Para colocar o app online, use um MySQL hospedado e configure `DATABASE_URL` nos secrets do Streamlit Community Cloud. A plataforma de hospedagem do banco pode ter custos ou limites de uso.

## Observação
Todos os dados são fictícios e destinados exclusivamente à demonstração.
