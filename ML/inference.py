import numpy as np
import pandas as pd
import ast
import joblib
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load the model and mappings
model = joblib.load(os.path.join(current_dir, 'final_model.pkl'))
category_mappings = joblib.load(os.path.join(current_dir, 'category_mappings.pkl'))
imputation_values = joblib.load(os.path.join(current_dir, 'imputation_values.pkl'))

# Preprocessing functions
def get_dictionary(s):
    try:
        d = eval(s)
    except:
        d = {}
    return d

def fix_date(x):
    if x > 2019:
        return x - 100
    else:
        return x

def preprocess_single_data(data):
    """
    Preprocess a single movie data dictionary and return the feature vector.
    
    data: dict with keys like 'release_date', 'genres', 'original_language', etc.
    """
    # Convert to DataFrame for easier processing
    df = pd.DataFrame([data])
    
    # Fill missing values
    df[['genres', 'original_language', 'spoken_languages', 'status', 'production_countries', 'production_companies', 'cast', 'crew']] = df[['genres', 'original_language', 'spoken_languages', 'status', 'production_countries', 'production_companies', 'cast', 'crew']].fillna("none")
    
    # Fix release date
    if pd.isna(df['release_date'].iloc[0]):
        df['release_date'] = '5/1/00'
    df['release_date'] = pd.to_datetime(df['release_date'], format='%m/%d/%y')
    
    # Create date features
    df["release_year"] = pd.to_datetime(df["release_date"]).dt.year.astype(int)
    df["release_day"] = pd.to_datetime(df["release_date"]).dt.dayofweek.astype(int)
    df["release_month"] = pd.to_datetime(df["release_date"]).dt.month.astype(int)
    
    # Fix years
    df['release_year'] = df['release_year'].apply(lambda x: fix_date(x))
    
    # Parse JSON fields
    df.genres = df.genres.map(lambda x: sorted([d['name'] for d in get_dictionary(x)])).map(lambda x: ','.join(map(str, x)))
    df.spoken_languages = df.spoken_languages.map(lambda x: sorted([d['name'] for d in get_dictionary(x)])).map(lambda x: ','.join(map(str, x)))
    df.cast = df.cast.map(lambda x: sorted([d['name'] for d in get_dictionary(x)])).map(lambda x: ','.join(map(str, x)))
    df.crew = df.crew.map(lambda x: sorted([d['name'] for d in get_dictionary(x)])).map(lambda x: ','.join(map(str, x)))
    
    # Count features
    df['genres_count'] = df['genres'].str.count(',') + 1
    df['spoken_languages_count'] = df['spoken_languages'].str.count(',') + 1
    df['cast_count'] = df['cast'].str.count(',') + 1
    df['crew_count'] = df['crew'].str.count(',') + 1
    
    # Encode categorical columns using saved mappings
    categorical_cols = ['status', 'original_language', 'production_companies', 'production_countries']
    for col in categorical_cols:
        cat_to_code = {cat: code for code, cat in category_mappings[col].items()}
        df[col] = df[col].map(cat_to_code).fillna(-1).astype(int)
    
    # Fill runtime and budget zeros
    df['runtime'] = df['runtime'].fillna(imputation_values['runtime_mean'])
    df['budget'] = df['budget'].replace(0, imputation_values['budget_mean'])
    df['runtime'] = df['runtime'].replace(0, imputation_values['runtime_mean'])
    
    # Select features
    feature_names = ['release_year', 'release_day', 'release_month', 'status', 'original_language',
                     'budget', 'popularity', 'genres_count', 'production_companies', 'production_countries',
                     'spoken_languages_count', 'cast_count', 'crew_count', 'runtime']
    
    X = df[feature_names]
    return X

def predict_revenue_processed(features):
    """
    Predict revenue using preprocessed features directly.
    
    features: dict with the 14 feature names
    returns: predicted revenue (float)
    """
    # Known category mappings (approximated)
    known_mappings = {
        'status': {'Post Production': 0, 'Released': 1, 'Rumored': 2},
        'original_language': {'en': 1, 'fr': 2, 'es': 3, 'de': 4, 'hi': 5},  # approximate
        'production_companies': {'Warner Bros.': 1, 'Universal Pictures': 2, 'Columbia Pictures': 3},  # approximate
        'production_countries': {'United States of America': 1, 'United Kingdom': 2, 'France': 3, 'Germany': 4, 'Canada': 5}  # approximate
    }
    
    # Convert to DataFrame
    df = pd.DataFrame([features])
    
    # Encode categorical columns
    categorical_cols = ['status', 'original_language', 'production_companies', 'production_countries']
    for col in categorical_cols:
        if col in known_mappings and features[col] in known_mappings[col] and features[col] != 'Other':
            df[col] = known_mappings[col][features[col]]
        else:
            df[col] = 0  # unknown or Other
    
    # Ensure order
    feature_names = ['release_year', 'release_day', 'release_month', 'status', 'original_language',
                     'budget', 'popularity', 'genres_count', 'production_companies', 'production_countries',
                     'spoken_languages_count', 'cast_count', 'crew_count', 'runtime']
    
    X = df[feature_names]
    
    # Predict
    y_pred_log = model.predict(X)
    y_pred = np.exp(y_pred_log)[0]
    return y_pred

# Example usage with the first test sample
if __name__ == "__main__":
    # Load one sample from test.csv
    test = pd.read_csv('./test.csv')
    sample_data = test.iloc[0].to_dict()
    print("Sample data for prediction:", sample_data)
    
    predicted_revenue = predict_revenue(sample_data)
    print(f"Predicted revenue for movie ID {sample_data['id']}: ${predicted_revenue:,.2f}")
    
    # For full test set (original functionality)
    # ... (rest of the original code for full prediction if needed)