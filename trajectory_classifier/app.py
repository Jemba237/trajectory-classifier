from flask import Flask
from flask import render_template
from flask import request
from config import *
import joblib
print(DB_HOST,DB_USER,DB_PASSWORD)
from services.predictor import predict

from services.database import (
    get_trajectory,
    get_all_trajectories,
    save_prediction
)

app = Flask(__name__)

le = joblib.load(
    "models/label_encoder.pkl"
)

print(le.classes_)

@app.route("/testdb")
def testdb():

    try:

        conn = get_connection()

        conn.close()

        return "DB OK"

    except Exception as e:

        return str(e)


@app.route("/")
def home():

    return render_template(
        "index.html",
        prediction=None,
        confidence=None
    )


@app.route(
    "/predict",
    methods=["POST"]
)
def predict_manual():

    data = {}

    fields = [

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

    for field in fields:

        if field == "type_equipement":

            equipment_name = request.form[field]

            data[field] = le.transform(
                [equipment_name]
            )[0]

        else:

            data[field] = float(
                request.form[field]
            )

    prediction, confidence = predict(
        data
    )

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence
    )


@app.route("/trajectories")
def trajectories():

    trajectories = get_all_trajectories()
    
    return render_template(
        "trajectories.html",
        trajectories=trajectories
    )
@app.route(
    "/predict-selected",
    methods=["POST"]
)
def predict_selected():

    ids = request.form.getlist(
        "trajectory_ids"
    )

    print("IDS :", ids)

    results = []

    for trajectory_id in ids:

        traj = get_trajectory(
            trajectory_id
        )

        equipment = traj["type_equipement"]

        if equipment not in le.classes_:

            print(
                f"Unknown equipment skipped: {equipment}"
            )

            continue

        encoded_equipment = le.transform(
            [equipment]
        )[0]

        traj["type_equipement"] = (
            encoded_equipment
        )

        prediction, confidence = predict(
            traj
        )

        best_confidence = max(
            confidence.values()
        )
        save_prediction(
            trajectory_id,
            prediction,
            best_confidence
        )
        results.append({

            "id": trajectory_id,
            "prediction": prediction,
            "confidence": best_confidence

        })

    print("RESULTS :", results)

    return render_template(
        "bulk_results.html",
        results=results
    )

# @app.route(
#     "/predict-selected",
#     methods=["POST"]
# )
# def predict_selected():
#     print("PREDICT SELECTED CLICKED")
#     ids = request.form.getlist(
#         "trajectory_ids"
#     )

#     results = []

#     for trajectory_id in ids:

#         traj = get_trajectory(
#             trajectory_id
#         )

#         encoded_equipment = le.transform([
#             traj["type_equipement"]
#         ])[0]

#         traj["type_equipement"] = (
#             encoded_equipment
#         )

#         prediction, confidence = predict(
#             traj
#         )

#         best_confidence = max(
#             confidence.values()
#         )

#         save_prediction(
#             trajectory_id,
#             prediction,
#             best_confidence
#         )

#         results.append({

#             "id": trajectory_id,
#             "prediction": prediction,
#             "confidence": best_confidence

#         })

#     return render_template(
#         "bulk_results.html",
#         results=results
#     )


if __name__ == "__main__":

    app.run(
        debug=True
    )
