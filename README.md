📊 SalesScope — Dashboard de Vendas
Dashboard interativo de Business Intelligence desenvolvido com Python, MySQL, Pandas, Streamlit e Plotly.

O SalesScope é um projeto de portfólio voltado à análise de desempenho comercial. O aplicativo transforma registros de vendas em indicadores e visualizações que ajudam a identificar tendências, comparar resultados e apoiar decisões de negócio.
Projeto demonstrativo: a base contém 3.000 pedidos fictícios gerados para fins de estudo. Os resultados não representam vendas reais de uma empresa.

🎯 Objetivo
Demonstrar competências práticas em SQL, modelagem e consulta de dados, análise exploratória, construção de KPIs e visualização de dados por meio de uma aplicação web interativa.
✨ Funcionalidades
- Indicadores comerciais: faturamento, lucro bruto estimado, quantidade de pedidos, ticket médio e margem bruta estimada.
- Filtros interativos: período, categoria e estado.
- Evolução temporal: acompanhamento do faturamento por mês e comparação de resultados entre períodos.
- Análise por segmento: faturamento por categoria e por estado.
- Ranking de produtos: produtos com maior faturamento, volume vendido e lucro bruto estimado.
- Tabela de pedidos: consulta detalhada dos registros filtrados.
- Exportação CSV: download dos dados filtrados para análises adicionais.
- Interface personalizada: tema escuro com detalhes dourados.
🛠️ Tecnologias
Tecnologia	Aplicação no projeto
Python	Lógica da aplicação e cálculos
MySQL	Armazenamento dos registros de vendas
SQL / SQLAlchemy / PyMySQL	Consulta e conexão ao banco de dados
Pandas	Tratamento, filtros e agregações
Streamlit	Interface web e componentes interativos
Plotly	Visualizações de dados
Git e GitHub	Versionamento e documentação


🧮 Indicadores e regras de cálculo
- Faturamento: quantidade × preço unitário.
- Lucro bruto estimado: quantidade × (preço unitário − custo unitário).
- Ticket médio: faturamento ÷ quantidade de pedidos distintos.
- Margem bruta estimada: lucro bruto estimado ÷ faturamento × 100.
Observação: o lucro bruto estimado não considera impostos, frete, despesas operacionais ou outras deduções.
🖥️ Capturas de tela
Adicione aqui imagens do dashboard em funcionamento. Sugestão de estrutura:
imagens/
├── dashboard-geral.png
├── graficos.png
└── tabela-pedidos.png
Após adicionar as imagens, substitua este trecho por:
![Visão geral do SalesScope](imagens/dashboard-geral.png)
![Gráficos de análise de vendas](imagens/graficos.png)
![Tabela detalhada de pedidos](imagens/tabela-pedidos.png)
🚀 Como executar localmente
Pré-requisitos
- Python 3.11 ou superior
- MySQL Server em execução
- Banco de dados MySQL acessível
1. Clonar o repositório
git clone https://github.com/Gustavo-010101/SalesScope-Dashboard-Vendas.git
cd SalesScope-Dashboard-Vendas
2. Criar o ambiente virtual e instalar as dependências
Windows (PowerShell):
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
3. Configurar o MySQL
Execute o script sql/schema.sql no MySQL Workbench para criar a estrutura de dados.

Crie um arquivo .env na raiz do projeto com a variável:
DATABASE_URL=mysql+pymysql://root:SUA_SENHA@localhost:3306/dashboard_vendas?charset=utf8mb4
Substitua SUA_SENHA por sua senha local. Se ela tiver caracteres especiais, codifique-os corretamente na URL. Nunca publique o arquivo .env ou credenciais reais.
4. Gerar os dados fictícios
.\.venv\Scripts\python.exe generate_data.py
Atenção: use um banco dedicado ao projeto. O script de geração pode substituir dados existentes na tabela de vendas.

5. Iniciar a aplicação
.\.venv\Scripts\python.exe -m streamlit run app.py
Abra o endereço exibido no terminal, geralmente http://localhost:8501.
📁 Estrutura do projeto
SalesScope-Dashboard-Vendas/
├── app.py                 # Interface e análises
├── database.py            # Conexão e leitura de dados do MySQL
├── generate_data.py       # Geração dos pedidos fictícios
├── requirements.txt       # Dependências Python
├── sql/
│   └── schema.sql         # Estrutura do banco de dados
├── .streamlit/             # Configuração visual (se incluída)
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore             # Arquivos excluídos do versionamento
└── README.md              # Documentação do projeto
📈 Competências demonstradas
- Construção de consultas e integração com banco de dados relacional.
- Limpeza, transformação e agregação de dados com Pandas.
- Definição e cálculo de indicadores de desempenho comercial.
- Visualização interativa e comunicação de resultados.
- Organização, documentação e versionamento de um projeto de dados.
🔮 Próximas melhorias
- Disponibilizar uma demonstração pública do aplicativo.
- Adicionar testes automatizados para as métricas.
- Implementar indicadores de metas comerciais e alertas.
- Aprimorar análises comparativas e segmentações.
👨‍💻 Autor
Gustavo — Projeto de portfólio para a área de Análise de Dados.

GitHub: @Gustavo-010101
Projeto desenvolvido para aprendizado e demonstração técnica. Todos os dados comerciais utilizados são fictícios.
