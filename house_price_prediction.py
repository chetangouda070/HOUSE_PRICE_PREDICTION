import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('housing.csv')
print(f"Dataset shape: {df.shape}")
print(f"Missing values: {df.isnull().sum().sum()}")

df = df.drop_duplicates()

X = df.drop('price', axis=1)
y = df['price']

categorical_cols = ['location']
numerical_cols = ['area', 'bedrooms', 'bathrooms', 'age']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_cols)
    ])

X_processed = preprocessor.fit_transform(X)

feature_names = numerical_cols.copy()
cat_encoder = preprocessor.named_transformers_['cat']
cat_feature_names = cat_encoder.get_feature_names_out(categorical_cols)
feature_names.extend(cat_feature_names)

X_df = pd.DataFrame(X_processed, columns=feature_names)
X_df['area_squared'] = X_df['area'] ** 2
X_df['area_bedrooms_interaction'] = X_df['area'] * X_df['bedrooms']
X_df['price_per_sqft_estimate'] = y.values / df['area'].values

engineered_feature_names = list(X_df.columns)
X_engineered = X_df.values

X_train, X_test, y_train, y_test = train_test_split(
    X_engineered, y, test_size=0.2, random_state=42
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Testing set: {X_test.shape[0]} samples")

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
}

results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    
    y_pred_train = model.predict(X_train)
    y_pred_test = model.predict(X_test)
    
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    
    results[name] = {
        'model': model,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'train_mae': train_mae,
        'test_mae': test_mae,
        'y_pred_test': y_pred_test
    }
    
    print(f"\n{name}:")
    print(f"  Test R²: {test_r2:.3f}")
    print(f"  Test RMSE: ${test_rmse:,.0f}")
    print(f"  Test MAE: ${test_mae:,.0f}")

best_model_name = max(results.keys(), key=lambda x: results[x]['test_r2'])
print(f"\nBest model: {best_model_name}")

cv = KFold(n_splits=5, shuffle=True, random_state=42)
cv_r2_scores = cross_val_score(results[best_model_name]['model'], X_engineered, y, cv=cv, scoring='r2')
cv_mae_scores = cross_val_score(results[best_model_name]['model'], X_engineered, y, cv=cv, scoring='neg_mean_absolute_error')
cv_mae_scores = -cv_mae_scores

print(f"\nCross-Validation Results (5-fold):")
print(f"  Mean R²: {cv_r2_scores.mean():.3f} ± {cv_r2_scores.std():.3f}")
print(f"  Mean MAE: ${cv_mae_scores.mean():,.0f} ± ${cv_mae_scores.std():,.0f}")

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
}

rf = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(
    rf, param_grid, cv=3, scoring='neg_mean_absolute_error', n_jobs=-1
)
grid_search.fit(X_train, y_train)

best_params = grid_search.best_params_
tuned_model = RandomForestRegressor(**best_params, random_state=42)
tuned_model.fit(X_train, y_train)

y_pred_tuned = tuned_model.predict(X_test)
tuned_r2 = r2_score(y_test, y_pred_tuned)
tuned_mae = mean_absolute_error(y_test, y_pred_tuned)

print(f"\nTuned model R²: {tuned_r2:.3f}")
print(f"Tuned model MAE: ${tuned_mae:,.0f}")

final_model = RandomForestRegressor(n_estimators=100, random_state=42)
pipeline = Pipeline([
    ('preprocessing', preprocessor),
    ('model', final_model)
])
pipeline.fit(df.drop('price', axis=1), y)

joblib.dump(pipeline, 'house_price_model.pkl')

metadata = {
    'model_type': 'Random Forest Regressor',
    'training_date': '2026-04-22',
    'dataset_info': {
        'samples': len(df),
        'features': len(engineered_feature_names),
        'feature_names': engineered_feature_names
    },
    'performance_metrics': {
        'test_r2': results[best_model_name]['test_r2'],
        'test_rmse': results[best_model_name]['test_rmse'],
        'test_mae': results[best_model_name]['test_mae'],
        'cross_validation_r2_mean': cv_r2_scores.mean(),
        'cross_validation_r2_std': cv_r2_scores.std()
    },
    'feature_importance': dict(zip(
        engineered_feature_names,
        results[best_model_name]['model'].feature_importances_
    )),
    'preprocessing_info': {
        'scaler': 'StandardScaler',
        'encoder': 'OneHotEncoder',
        'engineered_features': ['area_squared', 'area_bedrooms_interaction', 'price_per_sqft_estimate']
    }
}

joblib.dump(metadata, 'house_price_model_metadata.pkl')
print("\nModel saved as 'house_price_model.pkl'")
print("Metadata saved as 'house_price_model_metadata.pkl'")

print("\nTesting on sample predictions:")
test_houses = [
    {"area": 750, "bedrooms": 1, "bathrooms": 1, "location": "Urban", "age": 15},
    {"area": 1800, "bedrooms": 4, "bathrooms": 3, "location": "Suburb", "age": 8},
    {"area": 3000, "bedrooms": 5, "bathrooms": 4, "location": "Luxury", "age": 2},
]

for i, house in enumerate(test_houses, 1):
    house_df = pd.DataFrame([house])
    predicted_price = pipeline.predict(house_df)[0]
    price_per_sqft = predicted_price / house['area']
    print(f"House {i}: ${predicted_price:,.0f} (${price_per_sqft:.0f}/sqft)")
