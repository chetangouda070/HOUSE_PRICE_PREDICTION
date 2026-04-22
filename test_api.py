import requests
import json

test_house = {
    'area': 1500,
    'bedrooms': 3,
    'bathrooms': 2,
    'location': 'Urban',
    'age': 5
}

try:
    response = requests.post('http://localhost:8000/predict', json=test_house)
    print('Single prediction:')
    result = response.json()
    print(f'Predicted Price: ${result["predicted_price"]:,.0f}')
    print(f'Price per SqFt: ${result["price_per_sqft"]:.0f}')
except Exception as e:
    print(f'Single prediction failed: {e}')

batch_houses = {
    'houses': [
        {'area': 1200, 'bedrooms': 3, 'bathrooms': 2, 'location': 'Suburb', 'age': 10},
        {'area': 2000, 'bedrooms': 4, 'bathrooms': 3, 'location': 'Luxury', 'age': 2}
    ]
}

try:
    response = requests.post('http://localhost:8000/predict/batch', json=batch_houses)
    print('\nBatch prediction:')
    result = response.json()
    summary = result['summary']
    print(f'Houses: {summary["count"]}, Avg: ${summary["mean_price"]:,.0f}')
    for i, pred in enumerate(result['predictions']):
        print(f'House {i+1}: ${pred["predicted_price"]:,.0f}')
except Exception as e:
    print(f'Batch prediction failed: {e}')