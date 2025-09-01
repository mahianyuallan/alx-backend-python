#!/usr/bin/python3
"""
0-stream_users.py - Generator that streams rows from user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator function that streams rows from user_data table one by one.
    Yields each row as a dictionary.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # update if needed
            password="root",   # update if needed
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)  # results as dict
        cursor.execute("SELECT * FROM user_data;")

        for row in cursor:   # single loop
            yield row

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming users: {e}")
        return
