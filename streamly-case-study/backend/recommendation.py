import sqlite3
import pandas as pd
import math

# Path to the SQLite database
DB_PATH = "../streamly.db"

# -----------------------------
# Helper Functions
# -----------------------------

def parse_preferences(pref_str):
    """
    Convert a comma-separated string of preferences into a list.
    Returns an empty list if input is None or empty.
    """
    if pref_str is None or str(pref_str).strip() == "":
        return []
    return [p.strip() for p in str(pref_str).split(",")]

def allowed_ratings_for_age_band(age_band: str):
    """
    Return a list of allowed age ratings based on the profile's age band.
    This ensures age-appropriate content is recommended.
    """
    age_band = str(age_band)
    if age_band == "<13":
        return ["G", "PG"]
    elif age_band == "13-17":
        return ["G", "PG", "13+"]
    else:
        return ["G", "PG", "13+", "16+", "18+"]

def popularity_score(row):
    """
    Compute a simple popularity score for a title using:
      - IMDB rating (0-10) scaled by 2
      - Number of votes, transformed logarithmically
    This balances highly-rated content with audience size.
    """
    rating = row.get("imdb_rating", 0) or 0
    votes = row.get("imdb_votes", 0) or 0
    return rating * 2 + math.log1p(votes)

# -----------------------------
# Core Recommendation Function
# -----------------------------

def recommend_titles_for_profile(profile_id: int, n: int = 10):
    """
    Generate top N recommended titles for a given profile ID.

    Steps:
      1. Load profiles and titles from the SQLite database.
      2. Parse profile preferences into lists.
      3. Extract the profile's key features:
          - age band
          - kids profile flag
          - preferred language
          - preferred genres
      4. Compute allowed age ratings for the profile.
      5. Iterate through all titles and compute a recommendation score:
          - Age/content suitability
          - Kids vs non-kids content
          - Language match
          - Genre preference match
          - Popularity
      6. Sort titles by score and return top N results.
    """
    
    # Load data from database
    conn = sqlite3.connect(DB_PATH)
    profiles = pd.read_sql_query("SELECT * FROM profiles;", conn)
    titles = pd.read_sql_query("SELECT * FROM titles;", conn)
    conn.close()

    # Parse profile preferences into lists for easy genre matching
    profiles["preference_list"] = profiles["preferences"].apply(parse_preferences)

    # Fetch the target profile
    prof = profiles.loc[profiles["profile_id"] == profile_id]
    if prof.empty:
        return []  # Return empty list if profile not found

    prof = prof.iloc[0]

    # Extract profile features
    age_band = prof["age_band"]
    kids_profile = bool(prof["kids_profile"])
    pref_lang = prof["preferred_language"]
    pref_genres = set([p.lower() for p in prof["preference_list"]])

    # Determine allowed age ratings
    allowed_ratings = allowed_ratings_for_age_band(age_band)

    # Prepare a copy of titles to compute scores
    df = titles.copy()
    scores = []

    # Compute recommendation score for each title
    for _, row in df.iterrows():
        score = 0

        # Age/content suitability
        if row["age_rating"] in allowed_ratings:
            score += 40
        else:
            score -= 20

        # Kids vs non-kids content
        is_kids_title = bool(row["is_kids_content"])
        if kids_profile:
            if is_kids_title:
                score += 30
            else:
                score -= 100  # Hard penalty for unsuitable content
        else:
            if is_kids_title:
                score -= 5  # Slight penalty for adult profiles

        # Language match
        if str(row["language"]).lower() == str(pref_lang).lower():
            score += 30

        # Genre preference match
        cat = str(row["category"]).lower()
        subcat = str(row["sub_category"]).lower()
        title_genres = {cat, subcat}
        if pref_genres & title_genres:
            score += 25

        # Add popularity score
        score += popularity_score(row)

        scores.append(score)

    # Assign scores to the dataframe
    df["score"] = scores

    # Sort titles by score and select top N
    df_sorted = df.sort_values("score", ascending=False).head(n)

    # Return results in structured format
    results = df_sorted[["show_id", "title_name", "category", "age_rating", "language", "score"]]
    return results.to_dict(orient="records")