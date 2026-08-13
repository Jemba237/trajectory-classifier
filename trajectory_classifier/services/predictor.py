import joblib
import pandas as pd

rf = joblib.load(
    "models/random_forest.pkl"
)

FEATURES = [
    "duree_secondes",
    "distance_metres",
    "type_equipement",
    "saturations",
    "temp_min",
    "temp_max",
    "vibration_gRMS",
    "vitesse_rotation_max",
    "acceleration_max",
    "taux_rejection_spZupt",
    "taux_rejection_trZupt",
    "taux_rejection_GPSH",
    "taux_rejection_GPSV"
]


def predict(features_dict):

    model_data = {}

    for feature in FEATURES:
        model_data[feature] = features_dict[feature]

    df = pd.DataFrame([model_data])

    prediction = rf.predict(df)[0]

    probabilities = rf.predict_proba(df)[0]

    confidence = {

        cls: round(
            prob * 100,
            2
        )

        for cls, prob
        in zip(
            rf.classes_,
            probabilities
        )

    }

    return prediction, confidence