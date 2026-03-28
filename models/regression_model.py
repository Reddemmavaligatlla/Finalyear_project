# --------------------------------------------------
# LOGISTIC REGRESSION MODEL
# Predicts whether user will like a product
# --------------------------------------------------

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class PreferencePredictor:
    def __init__(self):
        self.model = LogisticRegression()

    def prepare_training_data(self):
        """
        Simulated training data
        """
        data = {
            "content_score": [0.9, 0.85, 0.3, 0.4, 0.75, 0.2, 0.8],
            "collab_score":  [0.8, 0.7, 0.2, 0.1, 0.6, 0.3, 0.75],
            "liked":         [1,   1,   0,   0,   1,   0,   1]
        }

        df = pd.DataFrame(data)
        X = df[["content_score", "collab_score"]]
        y = df["liked"]

        return X, y

    def train(self):
        X, y = self.prepare_training_data()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model.fit(X_train, y_train)

        preds = self.model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        print(f"✅ Logistic Regression Accuracy: {acc:.2f}")

    def predict_like_probability(self, content_score, collab_score):
        """
        Predict probability that user will like the product
        """
        prob = self.model.predict_proba([[content_score, collab_score]])[0][1]
        return prob


# ---------------- TEST ----------------
if __name__ == "__main__":
    predictor = PreferencePredictor()
    predictor.train()

    prob = predictor.predict_like_probability(
        content_score=0.8,
        collab_score=0.6
    )

    print(f"Predicted Like Probability: {prob:.2f}")
