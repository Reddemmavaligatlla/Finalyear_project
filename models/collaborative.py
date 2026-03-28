# --------------------------------------------------
# COLLABORATIVE FILTERING (USER-USER)
# Uses Cosine Similarity
# Preferences are treated as interaction data
# --------------------------------------------------

import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# LOAD USER PREFERENCES AS INTERACTIONS
# --------------------------------------------------
def load_user_preferences(json_path):
    """
    Loads user preferences from users.json
    and treats them as interaction data.
    """
    with open(json_path, "r") as f:
        users = json.load(f)

    interactions = {}

    for user_id, data in users.items():
        if "preferences" in data:
            interactions[user_id] = data["preferences"]

    return interactions


# --------------------------------------------------
# BUILD USER-ITEM MATRIX
# --------------------------------------------------
def build_user_item_matrix(interactions):
    """
    Converts interaction dictionary into
    a user-item matrix (DataFrame).
    """
    df = pd.DataFrame.from_dict(interactions, orient="index")
    df = df.stack().str.get_dummies().groupby(level=0).sum()
    return df


# --------------------------------------------------
# COMPUTE USER SIMILARITY
# --------------------------------------------------
def compute_user_similarity(user_item_matrix):
    similarity_matrix = cosine_similarity(user_item_matrix)

    similarity_df = pd.DataFrame(
        similarity_matrix,
        index=user_item_matrix.index,
        columns=user_item_matrix.index
    )

    return similarity_df


# --------------------------------------------------
# RECOMMEND BASED ON SIMILAR USERS
# --------------------------------------------------
def recommend_from_similar_users(
    user_id,
    users_json_path,
    top_n=5
):
    interactions = load_user_preferences(users_json_path)

    if user_id not in interactions:
        return []

    user_item_matrix = build_user_item_matrix(interactions)
    similarity_df = compute_user_similarity(user_item_matrix)

    similar_users = (
        similarity_df[user_id]
        .drop(user_id)
        .sort_values(ascending=False)
    )

    recommended = set()

    for similar_user in similar_users.index:
        for item in interactions.get(similar_user, []):
            if item not in interactions[user_id]:
                recommended.add(item)

        if len(recommended) >= top_n:
            break

    return list(recommended)[:top_n]


# --------------------------------------------------
# TEST
# --------------------------------------------------
if __name__ == "__main__":
    recs = recommend_from_similar_users(
        "u976",
        "data/users.json"
    )

    print("Collaborative Recommendations:", recs)
