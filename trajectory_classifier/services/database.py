import pymysql
from config import *


def get_connection():

 return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database="ExailPipeLAnd",
        cursorclass=pymysql.cursors.DictCursor
    )


def get_trajectory(trajectory_id):

    conn = get_connection()

    with conn.cursor() as cursor:

        cursor.execute(
            """
            SELECT *
            FROM trajectories
            WHERE id=%s
            """,
            (trajectory_id,)
        )

        result = cursor.fetchone()

    conn.close()

    return result


def get_all_trajectories():

    conn = get_connection()

    with conn.cursor() as cursor:

        cursor.execute(
            """
            SELECT *
            FROM trajectories
            ORDER BY date_acquisition DESC
            """
        )

        result = cursor.fetchall()

    conn.close()
    print(result[:2])
    return result


def save_prediction(
        trajectory_id,
        predicted_class,
        confidence
):

    conn = get_connection()

    with conn.cursor() as cursor:

        cursor.execute(
            """
            UPDATE trajectories
            SET
                predicted_class=%s,
                prediction_confidence=%s,
                prediction_date=NOW()
            WHERE id=%s
            """,
            (
                predicted_class,
                confidence,
                trajectory_id
            )
        )

    conn.commit()

    conn.close()
