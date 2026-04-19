from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load models safely
try:
    rf_model = joblib.load('movie_box_office_model.pkl')
    genre_means = joblib.load('genre_means.pkl')
    star_means = joblib.load('star_means.pkl')
except Exception as e:
    print("Error loading models. Make sure you've run model_pipeline.py first.")
    # mock fallback for development if models missing
    genre_means = pd.Series([1000, 2000], index=['Action', 'Comedy'])
    star_means = pd.Series([1000, 2000], index=['Tom Cruise', 'Brad Pitt'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/options', methods=['GET'])
def get_options():
    return jsonify({
        'genres': list(genre_means.index),
        'stars': list(star_means.index)
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.json
    
    budget = float(data.get('budget', 0))
    votes = float(data.get('votes', 0))
    runtime = float(data.get('runtime', 120))
    score = float(data.get('score', 5.0))
    genre = data.get('genre', '')
    star = data.get('star', '')

    genre_encoded = genre_means.get(genre, genre_means.mean())
    star_encoded = star_means.get(star, star_means.mean())
    
    X_input = pd.DataFrame({
        'budget': [budget],
        'votes': [votes],
        'runtime': [runtime],
        'score': [score],
        'genre_encoded': [genre_encoded],
        'star_encoded': [star_encoded]
    })
    
    prediction = rf_model.predict(X_input)[0]
    
    return jsonify({
        'predicted_earnings': prediction,
        'is_hit': bool(prediction > budget * 1.5),
        'is_profitable': bool(prediction > budget)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5050)
