import streamlit as st
import pandas as pd
import joblib

# Try loading trained model files
try:
    rf_model = joblib.load('movie_box_office_model.pkl')
    genre_means = joblib.load('genre_means.pkl')
    star_means = joblib.load('star_means.pkl')
except:
    rf_model = None
    # fallback data if model files are missing
    genre_means = pd.Series([1000, 2000, 1500], index=["Action", "Comedy", "Drama"])
    star_means = pd.Series([1000, 2000, 1500], index=["Actor A", "Actor B", "Actor C"])

# Page config
st.set_page_config(page_title="Movie Box Office Predictor", page_icon="🍿")

# Title
st.title("🎥 Movie Box Office Earnings Predictor")
st.markdown(
    "Welcome to the **Box Office Prediction Platform**! "
    "Enter the features of your movie to predict the gross earnings."
)

# Layout
col1, col2 = st.columns(2)

with col1:
    budget = st.number_input("Est. Budget ($)", min_value=0, value=25000000, step=1000000)
    runtime = st.number_input("Runtime (Minutes)", min_value=1, value=115)
    genre = st.selectbox("Genre", options=genre_means.index)

with col2:
    votes = st.number_input("Expected Votes on IMDB", min_value=0, value=150000, step=1000)
    score = st.slider("Expected Score (1.0 to 10.0)", min_value=1.0, max_value=10.0, value=7.2)
    star = st.selectbox("Lead Star (Cast)", options=star_means.index)

# Prediction button
if st.button("Predict Gross Earnings", type="primary"):

    # Encode inputs
    genre_encoded = genre_means.get(genre, genre_means.mean())
    star_encoded = star_means.get(star, star_means.mean())

    # Create input dataframe
    X_input = pd.DataFrame({
        'budget': [budget],
        'votes': [votes],
        'runtime': [runtime],
        'score': [score],
        'genre_encoded': [genre_encoded],
        'star_encoded': [star_encoded]
    })

    # Prediction logic
    if rf_model:
        prediction = rf_model.predict(X_input)[0]
    else:
        prediction = budget * 2  # fallback logic

    # Output
    st.success(f"**Predicted Box Office Earnings: ${prediction:,.2f}**")

    # Result interpretation
    if prediction > budget * 1.5:
        st.balloons()
        st.markdown("🎉 **Success!** This movie is predicted to be a **Box Office Hit!**")
    elif prediction > budget:
        st.info("✅ This movie is predicted to break even and turn a modest profit.")
    else:
        st.warning("⚠️ **Warning:** This movie might struggle to break even and could be a flop.")
