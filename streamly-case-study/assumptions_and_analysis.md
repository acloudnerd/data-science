# Streamly Case Study – Assumptions & Analysis

 

## 1. Data Assumptions

 

- Only `profiles.csv` and `titles.csv` were provided; no `accounts.csv` was available.

- Account-level information was inferred from `profiles.account_id`:

  - 1 profile per account → treated as "Basic"

  - 2–4 profiles per account → treated as "Premium"

- Missing `preferred_language` values in profiles were defaulted to `"English"`.

- IMDB rating and votes:

  - Some titles had null `imdb_rating` and/or `imdb_votes`.

  - Null IMDB values were handled safely in the scoring logic (no crashes).

  - Titles with missing IMDB data do not receive a strong popularity boost.

 

## 2. Data Cleaning Decisions

 

- Standardised string fields by trimming whitespace.

- Converted:

  - `kids_profile`, `is_kids_content` to booleans / integers.

  - IMDB columns and numeric metadata (`duration`, `year`, `episode_count`, etc.) to numeric types.

  - `created_at` to datetime.

- Deduplicated:

  - Profiles on `profile_id`

  - Titles on `show_id`

- Parsed `preferences` string field into a list of genres (e.g. `"Horror, Thriller"` → `["Horror", "Thriller"]`).

 

## 3. Database Design

 

- Chosen DB: SQLite for simplicity and portability.

- Tables:

  - `accounts(account_id, plan_type, profile_count, created_at)`

  - `profiles(profile_id, account_id, profile_name, kids_profile, age_band, preferred_language, created_at, preferences)`

  - `titles(show_id, title_name, category, sub_category, duration, age_rating, type, year, origin_region, language, episode_count, is_kids_content, imdb_rating, imdb_votes)`

- The database is generated programmatically via `notebooks/03_db_and_schema.ipynb`.

 

## 4. Recommendation Logic (Heuristic Approach)

 

- Implemented a heuristic scoring model (rule-based), not ML.

- Features considered:

  - Age-band vs age rating (safety & suitability)

  - Kids profile vs kids content

  - Language match between profile and title

  - Genre / category match based on profile preferences

  - IMDB-based popularity (rating + votes) as a tie-breaker

- The algorithm ranks titles per profile and returns the top N recommendations.

 

## 5. Why Not Machine Learning?

 

- The provided dataset does not include behavioural data (watch history, clicks, ratings).

- ML recommenders rely heavily on historical interactions.

- For this case study, a deterministic heuristic engine is:

  - More explainable

  - Easier to validate

  - Better aligned with the given data

 

## 6. How Machine Learning Could Be Introduced (Future Work)

 

- Once watch history is available, introduce:

  - Collaborative filtering (user–item interactions)

  - Content-based models (using genres, language, embeddings)

  - Hybrid recommendation (CF + content)

- Use current heuristic model as:

  - A candidate generator

  - A baseline for A/B testing

 

## 7. How to Reproduce

 

- Data exploration, cleaning, DB creation, and algorithm experimentation are captured in:

  - `01_data_exploration.ipynb`

  - `02_data_cleaning.ipynb`

  - `03_db_and_schema.ipynb`

  - `04_recommendation_algo.ipynb`