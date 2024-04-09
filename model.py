import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score,mean_absolute_error, median_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Charger les données depuis le fichier CSV
data = pd.read_csv('macrotrends.csv')

# Prétraitement des données
data['Growth Rate'] = data['Growth Rate'].str.rstrip('%').astype('float') / 100.0
data['Population Growth Rate'] = data['Population Growth Rate'].str.replace(',', '').astype('float')  # Supprimer les virgules et convertir en float
X = data[['Year', 'Growth Rate']]  # Features
y = data['Population Growth Rate']  # Target variable

# Séparation des données en ensembles d'entraînement et de test
X_train = X.iloc[25:]
X_test = X.iloc[:25]
y_train = y.iloc[25:]
y_test = y.iloc[:25]

# Standardisation des données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entraînement du modèle de régression linéaire
model = LinearRegression()
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Entraînement du modèle de régression Ridge
ridge_model = Ridge()
ridge_model.fit(X_train_scaled, y_train)
ridge_y_pred = ridge_model.predict(X_test_scaled)
ridge_mse = mean_squared_error(y_test, ridge_y_pred)
ridge_r2 = r2_score(y_test, ridge_y_pred)

# Entraînement du modèle de régression Lasso
lasso_model = Lasso()
lasso_model.fit(X_train_scaled, y_train)
lasso_y_pred = lasso_model.predict(X_test_scaled)
lasso_mse = mean_squared_error(y_test, lasso_y_pred)
lasso_r2 = r2_score(y_test, lasso_y_pred)

# Entraînement du modèle de régression ElasticNet
elasticnet_model = ElasticNet()
elasticnet_model.fit(X_train_scaled, y_train)
elasticnet_y_pred = elasticnet_model.predict(X_test_scaled)
elasticnet_mse = mean_squared_error(y_test, elasticnet_y_pred)
elasticnet_r2 = r2_score(y_test, elasticnet_y_pred)

# Entraînement du modèle de forêts aléatoires
random_forest_model = RandomForestRegressor()
random_forest_model.fit(X_train_scaled, y_train)
random_forest_y_pred = random_forest_model.predict(X_test_scaled)
random_forest_mse = mean_squared_error(y_test, random_forest_y_pred)
random_forest_r2 = r2_score(y_test, random_forest_y_pred)

results = pd.DataFrame({'Year': X_test['Year'], 
                        'Linear Regression': y_pred,
                        'Ridge Regression': ridge_y_pred,
                        'Lasso Regression': lasso_y_pred,
                        'ElasticNet Regression': elasticnet_y_pred,
                        'Random Forest': random_forest_y_pred})

results.to_csv('prediction.csv', index=False)


metrics_data = {
    'Algorithm': ['Linear Regression', 'Ridge Regression', 'Lasso Regression', 'ElasticNet Regression', 'Random Forest'],
    'Mean Squared Error': [mse, ridge_mse, lasso_mse, elasticnet_mse, random_forest_mse],
    'Mean Absolute Error': [mean_absolute_error(y_test, y_pred), mean_absolute_error(y_test, ridge_y_pred),
                            mean_absolute_error(y_test, lasso_y_pred), mean_absolute_error(y_test, elasticnet_y_pred),
                            mean_absolute_error(y_test, random_forest_y_pred)],
    'Median Absolute Error': [median_absolute_error(y_test, y_pred), median_absolute_error(y_test, ridge_y_pred),
                              median_absolute_error(y_test, lasso_y_pred), median_absolute_error(y_test, elasticnet_y_pred),
                              median_absolute_error(y_test, random_forest_y_pred)],
    'R-squared': [r2, ridge_r2, lasso_r2, elasticnet_r2, random_forest_r2]
}

metrics_df = pd.DataFrame(metrics_data)

metrics_df.to_csv('metrics.csv', index=False)
