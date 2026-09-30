# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
superkart_sales_application_api = Flask("superkart_sales_application")

# Load the trained machine learning model
model = joblib.load("superkart_sales_model.joblib")

# Define a route for the home page (GET request)
@superkart_sales_application_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the R API!"

# Define an endpoint for single property prediction (POST request)
@superkart_sales_application_api.post('/v1/predict')
def predict_sales_price():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing property details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': kart_data['Product_Weight'],
        'Product_Sugar_Content': kart_data['Product_Sugar_Content'],
        'Product_Allocated_Area': kart_data['Product_Allocated_Area'],
        'Product_MRP': kart_data['Product_MRP'],
        'Store_Size': kart_data['Store_Size'],
        'Store_Location_City_Type': kart_data['Store_Location_City_Type'],
        'Store_Type': kart_data['Store_Type'],
        'Store_Age_Years': kart_data['Store_Age_Years'],
        'Product_Type_Category': kart_data['Product_Type_Category'],
        'Product_Id_char': kart_data['Product_Id_char']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_log_price = model.predict(input_data)[0]

    # Calculate actual price
    predicted_price = np.exp(predicted_log_price)

    # Convert predicted_price to Python float
    predicted_price = round(float(predicted_price), 2)
    # The conversion above is needed as we convert the model prediction (log price) to actual price using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual price
    return jsonify({'Predicted Price (in dollars)': predicted_price})

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    superkart_sales_application_api.run(debug=True)
