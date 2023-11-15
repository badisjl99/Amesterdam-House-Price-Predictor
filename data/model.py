from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

df = pd.read_csv('dataset.csv')

df['Zip'] = df['Zip'].str.extract('(\d+)').astype(float)

default_value = 0

df['Zip'] = df['Zip'].fillna(default_value)

df = df.dropna(subset=['Price'])

X = df[['Zip', 'Area', 'Room']]
y = df['Price']

model = make_pipeline(StandardScaler(), LinearRegression())

model.fit(X, y)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    zip_code = data['zip']
    area = float(data['area'])
    room = float(data['room'])

    zip_numeric = pd.to_numeric(df['Zip'], errors='coerce')
    df['Zip'] = zip_numeric.fillna(default_value)

    new_data = pd.DataFrame([[zip_code, area, room]], columns=['Zip', 'Area', 'Room'])

    zip_code_processed = new_data['Zip'].iloc[0]

    new_data['Zip'] = zip_code_processed
    predicted_price = model.predict(new_data)

    return jsonify({'predicted_price': predicted_price[0]})

if __name__ == '__main__':
    app.run(port=5000)
