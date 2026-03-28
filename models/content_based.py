# ---------------------------------------------
# CONTENT-BASED RECOMMENDATION SYSTEM
# Uses TF-IDF Vectorization + Cosine Similarity
# ---------------------------------------------

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ------------------------------------------------
# STEP 1: LOAD PRODUCT DATA FROM CSV
# ------------------------------------------------
def load_products(csv_path):
    """
    Loads product data from CSV and keeps
    only required columns for recommendation.
    """
    df = pd.read_csv(csv_path)

    # Keep only relevant columns
    df = df[["product_id", "product_name", "category"]].drop_duplicates()

    return df


# ------------------------------------------------
# STEP 2: BUILD TF-IDF MATRIX FOR PRODUCT CATEGORIES
# ------------------------------------------------
def build_tfidf_matrix(categories):
    """
    Converts product categories (text)
    into TF-IDF vectors.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(categories)

    return tfidf_matrix, vectorizer


# ------------------------------------------------
# STEP 3: BUILD USER VECTOR FROM PREFERENCES
# ------------------------------------------------
def build_user_vector(preferences, vectorizer):
    """
    Converts user preference list into
    a single TF-IDF vector.
    """
    user_text = " ".join(preferences)
    user_vector = vectorizer.transform([user_text])

    return user_vector


# ------------------------------------------------
# STEP 4: RECOMMEND PRODUCTS USING COSINE SIMILARITY
# ------------------------------------------------
def recommend_products(csv_path, user_preferences, top_n=5):
    """
    Generates top-N product recommendations
    based on cosine similarity.
    """

    # Load products
    df = load_products(csv_path)

    # Build TF-IDF vectors for product categories
    tfidf_matrix, vectorizer = build_tfidf_matrix(df["category"])

    # Build TF-IDF vector for user preferences
    user_vector = build_user_vector(user_preferences, vectorizer)

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(user_vector, tfidf_matrix)[0]

    # Add similarity score to dataframe
    df["similarity"] = similarity_scores

    # Sort products by similarity score
    recommendations = (
        df.sort_values(by="similarity", ascending=False)
          .head(top_n)
    )

    return recommendations


# ------------------------------------------------
# STEP 5: TEST THE MODEL (ONLY FOR DEVELOPMENT)
# ------------------------------------------------
if __name__ == "__main__":
    user_prefs = ["Electronics", "Books"]

    recs = recommend_products(
        "data/ecommerce_dataset_cleaned.csv",
        user_prefs
    )

    print(recs[["product_name", "category", "similarity"]])
