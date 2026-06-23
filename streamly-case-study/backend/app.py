from flask import Flask, request, jsonify, send_from_directory
from recommendation import recommend_titles_for_profile
import sqlite3
import pandas as pd
import os

# -----------------------------
# Flask Application Setup
# -----------------------------
# Initialize Flask app
# 'static_folder' points to the frontend build folder
# 'static_url_path' allows serving static files from root URL
app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Path to the SQLite database
DB_PATH = "../streamly.db"

# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def index():
    """
    Serve the main frontend page (index.html).
    This is the landing page of the recommendation demo UI.
    """
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/profiles")
def list_profiles():
    """
    API endpoint to return a list of profiles.
    Returns profile_id, profile_name, age_band, and kids_profile flag.
    Used by frontend to populate the profile selection dropdown.
    """
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)

    # Query relevant profile information
    df = pd.read_sql_query(
        "SELECT profile_id, profile_name, age_band, kids_profile FROM profiles;", conn
    )
    conn.close()

    # Return as JSON
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/recommendations")
def recommendations():
    """
    API endpoint to return top 10 recommended titles for a given profile.
    Expects 'profile_id' as a query parameter.
    Calls the core recommendation function and returns results as JSON.
    """
    profile_id = request.args.get("profile_id", type=int)

    # Handle missing profile_id
    if profile_id is None:
        return jsonify({"error": "profile_id is required"}), 400

    # Generate recommendations
    recs = recommend_titles_for_profile(profile_id, n=10)

    # Return recommendations as JSON
    return jsonify(recs)

# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    # Start Flask development server
    # Accessible at http://127.0.0.1:5000
    # Debug mode enabled for live reloading during development
    app.run(host="127.0.0.1", port=5000, debug=True)