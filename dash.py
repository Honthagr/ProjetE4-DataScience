import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

digits = load_digits()
X = digits.data
y = digits.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=100),
    "Support Vector Machine": SVC()
}

results = {'Modèle': [], 'Précision': [], 'Rappel': [], 'F1-score': []}
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    results['Modèle'].append(name)
    results['Précision'].append(accuracy)
    results['Rappel'].append(recall)
    results['F1-score'].append(f1)

df = pd.DataFrame(results)

# Dash application
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Comparaison des modèles d'apprentissage sur le dataset MNIST"),
    html.Div([
        dcc.Dropdown(
            id='dropdown-metric',
            options=[
                {'label': 'Précision', 'value': 'Précision'},
                {'label': 'Rappel', 'value': 'Rappel'},
                {'label': 'F1-score', 'value': 'F1-score'}
            ],
            value='Précision'
        ),
        dcc.Graph(id='model-comparison')
    ])
])

# Callback to update the graph based on the selected metric
@app.callback(
    Output('model-comparison', 'figure'),
    [Input('dropdown-metric', 'value')]
)
def update_figure(metric):
    trace = []
    for model in df['Modèle']:
        trace.append(go.Bar(
            x=[model],
            y=[df[df['Modèle'] == model][metric].values[0]],
            name=model
        ))

    return {
        'data': trace,
        'layout': go.Layout(
            title=f"Comparaison des modèles selon la métrique : {metric}",
            xaxis={'title': 'Modèles'},
            yaxis={'title': metric}
        )
    }

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
