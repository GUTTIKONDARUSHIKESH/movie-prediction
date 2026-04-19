# Movie Box Office Earnings Predictor

A machine learning project that estimates **theatrical gross revenue** for a film from budget, runtime, expected IMDb engagement (votes and score), genre, and lead star. It ships with two ways to use the model: a **Flask** web app with a custom “Stellar” UI, and a **Streamlit** dashboard.

---

## Features

- **Random Forest regression** trained on historical movie data (budget, votes, runtime, score, genre, star → gross).
- **Target encoding** for categorical fields: each genre and lead star is mapped to the mean gross observed for that category in the training set (stored as `genre_means.pkl` and `star_means.pkl`).
- **Flask API** (`server.py`): JSON prediction endpoint and a single-page app that loads genre/star options dynamically.
- **Streamlit app** (`app.py`): interactive inputs, predicted dollar gross, and simple “hit / profitable / flop risk” messaging with optional celebratory UI when the prediction looks strong.
- **Training pipeline** (`model_pipeline.py`): downloads the dataset, cleans rows, fits the model, prints train/test R², and writes the `.pkl` artifacts.

---

## Tech Stack

| Area | Technology |
|------|------------|
| Language | Python 3 |
| ML | scikit-learn (`RandomForestRegressor`), pandas, numpy, joblib |
| Web (primary UI) | Flask, Jinja2 templates, vanilla JavaScript, CSS |
| Alternate UI | Streamlit |

---

## Project Structure

```
rishi project/
├── model_pipeline.py          # Train model; downloads data; saves .pkl files
├── server.py                  # Flask app (port 5050 by default)
├── app.py                     # Streamlit UI
├── movie_box_office_model.pkl # Trained model (created after training)
├── genre_means.pkl            # Target-encoded genre statistics
├── star_means.pkl             # Target-encoded star statistics
├── templates/
│   └── index.html             # Flask “Stellar” landing page
└── static/
    ├── style.css              # Layout and glassmorphism styling
    └── script.js              # Form submit, /api/options, /api/predict
```

The `.pkl` files are **not** guaranteed to be in the repository; run `model_pipeline.py` once to generate them.

---

## Prerequisites

- **Python 3.8+** recommended  
- **Internet access** when running `model_pipeline.py` (dataset is downloaded from a public URL)

---

## Dependencies

Install packages used across the pipeline and apps:

```bash
pip install pandas numpy scikit-learn joblib flask streamlit
```

---

## Quick Start

### 1. Train the model and create artifacts

From the project directory:

```bash
python model_pipeline.py
```

This will:

1. Download the dataset from:  
   `https://raw.githubusercontent.com/danielgrijalva/movie-stats/master/movies.csv`
2. Drop rows with missing values in `gross`, `budget`, `votes`, `runtime`, `genre`, `star`, or `score`.
3. Build target encodings for `genre` and `star` from grouped mean gross.
4. Split data (85% train / 15% test, `random_state=42`), train a `RandomForestRegressor` (`n_estimators=300`, `max_depth=None`, `min_samples_split=2`).
5. Print **train** and **test** R² scores and save:
   - `movie_box_office_model.pkl`
   - `genre_means.pkl`
   - `star_means.pkl`

### 2. Run the Flask web app (Stellar UI)

```bash
python server.py
```

Open a browser at **http://127.0.0.1:5050/** (debug mode is enabled in code).

The page loads genres and stars from `GET /api/options` and submits predictions to `POST /api/predict`.

### 3. Run the Streamlit app (optional)

```bash
streamlit run app.py
```

If the `.pkl` files are missing, Streamlit shows an error and tells you to run `model_pipeline.py` first.

---

## API Reference (Flask)

Base URL when running locally: `http://127.0.0.1:5050`

### `GET /api/options`

Returns the lists used to populate genre and star dropdowns (derived from the saved encoders).

**Response (JSON):**

```json
{
  "genres": ["Action", "Comedy", "..."],
  "stars": ["Actor A", "Actor B", "..."]
}
```

### `POST /api/predict`

**Request body (JSON):**

| Field | Type | Description |
|-------|------|-------------|
| `budget` | number | Production budget (USD) |
| `votes` | number | Expected IMDb vote count |
| `runtime` | number | Length in minutes |
| `score` | number | Expected IMDb score (1.0–10.0) |
| `genre` | string | Must match a value from `/api/options` for best results |
| `star` | string | Lead star; should match `/api/options` when possible |

**Response (JSON):**

| Field | Type | Meaning |
|-------|------|---------|
| `predicted_earnings` | number | Predicted gross (same units as training target) |
| `is_hit` | boolean | `true` if predicted gross > 1.5 × budget |
| `is_profitable` | boolean | `true` if predicted gross > budget |

Unknown genre or star values fall back to the **mean** of the respective encoder series when encoding for the model.

---

## Model Details

- **Algorithm:** Random Forest Regressor.
- **Features (order used at inference):**  
  `budget`, `votes`, `runtime`, `score`, `genre_encoded`, `star_encoded`.
- **Target:** `gross` from the movie-stats CSV.

The training script intentionally uses a deep forest configuration; **test R²** (printed after training) is the main indicator of generalization. Treat predictions as **demonstrations**, not financial advice.

---

## UI Behavior

### Flask (“Stellar”)

- Form fields: budget, runtime, votes, score, genre, lead star.
- After submit, shows predicted gross (USD, formatted) and a badge:
  - **Blazing hit** — `is_hit`
  - **Profitable** — `is_profitable` but not hit
  - **Flop risk** — otherwise

### Streamlit

- Similar inputs; on predict, shows dollar amount and short text (hit / modest profit / flop risk). Balloons appear when the model predicts a strong result vs. budget.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| “Model files not found” (Streamlit) or prediction errors | Run `python model_pipeline.py` in the project folder so all `.pkl` files exist next to the scripts. |
| Flask starts but predictions fail | Ensure `movie_box_office_model.pkl` exists; without it the app may not load the regressor correctly. |
| Empty or wrong dropdowns | Regenerate `genre_means.pkl` / `star_means.pkl` by retraining. |
| Training needs network | `model_pipeline.py` must reach GitHub raw content to download `movies.csv`. |

---

## Data Source

Training data is loaded from the **movie-stats** dataset (Daniel Grijalva) via the URL embedded in `model_pipeline.py`. Credit and license for that dataset follow the upstream repository’s terms.

---

## License

This README describes the project as provided. If you publish the repo, add a `LICENSE` file that matches your intent and any obligations from the dataset you use.
