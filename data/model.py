from flask import Flask, request, jsonify
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

# Read the dataset
df = pd.read_csv('dataset.csv')

# Handle non-numeric values in the 'Zip' column
df['Zip'] = df['Zip'].str.extract('(\d+)').astype(float)

# Define a default value to replace missing values in the 'Zip' column
default_value = 0  # Replace '0' with your desired default value

# Handle missing values in the 'Zip' column
df['Zip'] = df['Zip'].fillna(default_value)

# Drop rows with NaN values in the target variable ('Price')
df = df.dropna(subset=['Price'])

# Extract features (X) and target variable (y)
X = df[['Zip', 'Area', 'Room']]
y = df['Price']

# Create a pipeline with standardization and linear regression
model = make_pipeline(StandardScaler(), LinearRegression())

# Train the model
model.fit(X, y)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Extract input values from the request
    zip_code = data['zip']
    area = float(data['area'])
    room = float(data['room'])
    
    # Ensure the 'zip' column is numeric
    zip_numeric = pd.to_numeric(df['Zip'], errors='coerce')
    df['Zip'] = zip_numeric.fillna(default_value)
    
    new_data = pd.DataFrame([[zip_code, area, room]], columns=['Zip', 'Area', 'Room'])
    
    # Extract the processed 'Zip' value
    zip_code_processed = new_data['Zip'].iloc[0]
    
    # Use the processed 'Zip' value to make predictions
    new_data['Zip'] = zip_code_processed
    predicted_price = model.predict(new_data)
    
    return jsonify({'predicted_price': predicted_price[0]})

if __name__ == '__main__':
    app.run(port=5000)
