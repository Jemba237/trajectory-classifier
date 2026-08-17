import pymysql
from config import *


import pymysql
import ssl
import os

def get_connection():

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl={"ssl": {}},
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=30
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
