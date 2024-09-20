from sqlalchemy import create_engine
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import joblib  # Import joblib directly
from nltk.tokenize import word_tokenize
import requests

# Set up the database connection
engine = create_engine('postgresql+psycopg2://postgres:JHOAG@localhost:5432/palm_database')

# Load data from the database
business_units_df = pd.read_sql('SELECT * FROM businessunits', engine)
ar_data_df = pd.read_sql('SELECT * FROM accountsreceivable', engine)
payments_ledger_df = pd.read_sql('SELECT * FROM payments_ledger', engine)
invoices_ledger_df = pd.read_sql('SELECT * FROM invoices_ledger', engine)
expenses_ledger_df = pd.read_sql('SELECT * FROM expenses_ledger', engine)
budget_ledger_df = pd.read_sql('SELECT * FROM budget_ledger', engine)
payables_ledger_df = pd.read_sql('SELECT * FROM payables_ledger', engine)
assets_ledger_df = pd.read_sql('SELECT * FROM assets_ledger', engine)
liabilities_ledger_df = pd.read_sql('SELECT * FROM liabilities_ledger', engine)
revenue_ledger_df = pd.read_sql('SELECT * FROM revenue_ledger', engine)
equity_ledger_df = pd.read_sql('SELECT * FROM equity_ledger', engine)
cashflow_ledger_df = pd.read_sql('SELECT * FROM cashflow_ledger', engine)
networth_ledger_df = pd.read_sql('SELECT * FROM networth_ledger', engine)
pending_payables_ledger_df = pd.read_sql('SELECT * FROM pending_payables_ledger', engine)

# Ensure the date columns are in datetime format
expenses_ledger_df['expense_date'] = pd.to_datetime(expenses_ledger_df['expense_date'])
cashflow_ledger_df['transaction_date'] = pd.to_datetime(cashflow_ledger_df['transaction_date'])

# Create dummy data for new tabs
# Creating dummy data for Case Management
case_management_data = {
    'case_id': range(1, 101),
    'case_name': [f'Case {i}' for i in range(1, 101)],
    'status': np.random.choice(['Open', 'In Progress', 'Closed', 'On Hold'], 100),
    'assigned_user': np.random.choice(['User A', 'User B', 'User C', 'User D'], 100),
    'date_opened': pd.date_range(start='2023-01-01', periods=100, freq='B'),
    'date_closed': pd.date_range(start='2023-02-01', periods=100, freq='B')
}

case_management_df = pd.DataFrame(case_management_data)

# Creating dummy data for CRM Management
crm_management_data = {
    'customer_id': range(1, 201),
    'customer_name': [f'Customer {i}' for i in range(1, 201)],
    'interaction_type': np.random.choice(['Call', 'Email', 'Meeting', 'Social Media'], 200),
    'interaction_date': pd.date_range(start='2023-01-01', periods=200, freq='D'),
    'engagement_score': np.random.randint(1, 100, 200)
}

crm_management_df = pd.DataFrame(crm_management_data)

# Creating dummy data for Reports
reports_data = {
    'report_id': range(1, 51),
    'metric': np.random.choice(['Revenue', 'Expenses', 'Profit', 'Customer Growth'], 50),
    'value': np.random.randint(1000, 100000, 50),
    'date': pd.date_range(start='2023-01-01', periods=50, freq='W')
}

reports_df = pd.DataFrame(reports_data)

# Initialize the Dash app
app = Dash(__name__)

# Load ML model
model = joblib.load('your_model.pkl')  # Replace with the actual path to your model file

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1("Accounts Receivable Dashboard"),
    dcc.Tabs(id='tabs', value='tab-dashboard', children=[
        dcc.Tab(label='Dashboard', value='tab-dashboard'),
        dcc.Tab(label='Accounts Receivable Management', value='tab-ar', children=[
            dcc.Tabs(id='sub-tabs-ar', value='sub-tab-receivables', children=[
                dcc.Tab(label='Receivables Management', value='sub-tab-receivables'),
                dcc.Tab(label='Payments', value='sub-tab-payments'),
                dcc.Tab(label='Invoices', value='sub-tab-invoices'),
                dcc.Tab(label='Pending Payables', value='sub-tab-pending-payables')
            ])
        ]),
        dcc.Tab(label='Case Management', value='tab-case'),
        dcc.Tab(label='CRM Management', value='tab-crm'),
        dcc.Tab(label='Reports', value='tab-reports'),
        dcc.Tab(label='Settings', value='tab-settings'),
        dcc.Tab(label='Expenses', value='tab-expenses'),
        dcc.Tab(label='Budget', value='tab-budget'),
        dcc.Tab(label='Payables', value='tab-payables'),
        dcc.Tab(label='Assets', value='tab-assets'),
        dcc.Tab(label='Liabilities', value='tab-liabilities'),
        dcc.Tab(label='Revenue', value='tab-revenue'),
        dcc.Tab(label='Equity', value='tab-equity'),
        dcc.Tab(label='Cash Flow', value='tab-cashflow'),
        dcc.Tab(label='Net Worth', value='tab-networth')
    ]),
    html.Div(id='tabs-content'),

    # Data Export Button
    html.Button("Download Data", id="download-button"),
    dcc.Download(id="download-data"),

    # Sortable and Searchable Table
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in ar_data_df.columns],
        data=ar_data_df.to_dict('records'),
        sort_action='native',
        filter_action='native',
        editable=True
    ),

    # Advanced Filtering Options
    dcc.Dropdown(
        id='multi-filter',
        options=[
            {'label': 'Invoice Status', 'value': 'status'},
            {'label': 'Date Range', 'value': 'date_range'},
        ],
        multi=True
    ),

    # ML Prediction Section
    dcc.Input(id='input-parameters', type='text', placeholder='Enter parameters for prediction'),
    html.Div(id='prediction-output'),

    # NLP Search
    dcc.Input(id='nlp-search', type='text', placeholder='Search with Natural Language'),
    html.Div(id='search-results'),

    # API Data Fetching Section
    html.Button("Fetch External Data", id='fetch-button'),
    html.Div(id='api-data')
])

# Define callback to update the content based on tab and sub-tab selected
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value'), Input('sub-tabs-ar', 'value')])
def render_content(tab, sub_tab):
    if tab == 'tab-dashboard':
        return html.Div([
            html.H3('Dashboard Overview'),
            dcc.Graph(id='ar-by-unit-chart', figure=create_ar_by_unit_chart())
        ])
    elif tab == 'tab-ar':
        if sub_tab == 'sub-tab-receivables':
            return html.Div([
                html.H3('Receivables Management'),
                dcc.Graph(id='receivables-chart', figure=create_receivables_chart())
            ])
        elif sub_tab == 'sub-tab-payments':
            return html.Div([
                html.H3('Payments'),
                dcc.Graph(id='payments-chart', figure=create_payments_chart())
            ])
        elif sub_tab == 'sub-tab-invoices':
            return html.Div([
                html.H3('Invoices'),
                dcc.Graph(id='invoices-chart', figure=create_invoices_chart())
            ])
        elif sub_tab == 'sub-tab-pending-payables':
            return html.Div([
                html.H3('Pending Payables'),
                dcc.Graph(id='pending-payables-chart', figure=create_pending_payables_chart())
            ])
    elif tab == 'tab-case':
        return html.Div([
            html.H3('Case Management'),
            dcc.Graph(id='case-management-chart', figure=create_case_management_chart())
        ])
    elif tab == 'tab-crm':
        return html.Div([
            html.H3('CRM Management'),
            dcc.Graph(id='crm-management-chart', figure=create_crm_management_chart())
        ])
    elif tab == 'tab-reports':
        return html.Div([
            html.H3('Reports'),
            dcc.Graph(id='reports-chart', figure=create_reports_chart())
        ])
    elif tab == 'tab-settings':
        return html.Div([
            html.H3('Settings'),
            html.Div([
                html.Label('Username:'),
                dcc.Input(type='text', placeholder='Enter Username'),
                html.Label('Password:'),
                dcc.Input(type='password', placeholder='Enter Password'),
                html.Button('Submit', id='submit-settings')
            ]),
        ])
    elif tab == 'tab-expenses':
        return html.Div([
                        html.H3('Expenses'),
            dcc.Graph(id='expenses-chart', figure=create_expenses_chart())
        ])
    elif tab == 'tab-budget':
        return html.Div([
            html.H3('Budget'),
            dcc.Graph(id='budget-chart', figure=create_budget_chart())
        ])
    elif tab == 'tab-payables':
        return html.Div([
            html.H3('Payables'),
            dcc.Graph(id='payables-chart', figure=create_payables_chart())
        ])
    elif tab == 'tab-assets':
        return html.Div([
            html.H3('Assets'),
            dcc.Graph(id='assets-chart', figure=create_assets_chart())
        ])
    elif tab == 'tab-liabilities':
        return html.Div([
            html.H3('Liabilities'),
            dcc.Graph(id='liabilities-chart', figure=create_liabilities_chart())
        ])
    elif tab == 'tab-revenue':
        return html.Div([
            html.H3('Revenue'),
            dcc.Graph(id='revenue-chart', figure=create_revenue_chart())
        ])
    elif tab == 'tab-equity':
        return html.Div([
            html.H3('Equity'),
            dcc.Graph(id='equity-chart', figure=create_equity_chart())
        ])
    elif tab == 'tab-cashflow':
        return html.Div([
            html.H3('Cash Flow'),
            dcc.Graph(id='cashflow-chart', figure=create_cashflow_chart())
        ])
    elif tab == 'tab-networth':
        return html.Div([
            html.H3('Net Worth'),
            dcc.Graph(id='networth-chart', figure=create_networth_chart())
        ])

# Callbacks for additional functionalities

# Data export callback
@app.callback(
    Output("download-data", "data"),
    Input("download-button", "n_clicks"),
    prevent_initial_call=True
)
def download_data(n_clicks):
    return dcc.send_data_frame(ar_data_df.to_csv, "ar_data.csv")

# Machine learning prediction callback
@app.callback(
    Output('prediction-output', 'children'),
    Input('input-parameters', 'value')
)
def make_prediction(input_parameters):
    # Assuming input_parameters is a comma-separated string of values
    parameters = np.array([float(i) for i in input_parameters.split(',')]).reshape(1, -1)
    prediction = model.predict(parameters)
    return f"Predicted Value: {prediction[0]}"

# NLP search callback
@app.callback(
    Output('search-results', 'children'),
    Input('nlp-search', 'value')
)
def nlp_search(query):
    tokens = word_tokenize(query.lower())
    # Implement your NLP logic for search and filtering
    # For demonstration purposes, we just return the tokens
    return f"Search tokens: {tokens}"

# Fetch data from external API callback
@app.callback(
    Output('api-data', 'children'),
    Input('fetch-button', 'n_clicks'),
    prevent_initial_call=True
)
def fetch_external_data(n_clicks):
    response = requests.get('https://api.example.com/data')  # Replace with the actual API URL
    if response.status_code == 200:
        data = response.json()
        return f"Fetched data: {data}"
    else:
        return "Failed to fetch data from the API."

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
