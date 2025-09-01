#!/usr/bin/python3
"""
1-batch_processing.py - Stream and process users in batches
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data in batches.
    Yields each batch as a list of dictionaries.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # update if needed
            password="root",    # update if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")

        batch = []
        for row in cursor:  # loop #1
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch  # last incomplete batch

        cursor.close()
        connection.close()

    except Error as e:
        print(f"Error streaming batches: {e}")
        return


def batch_processing(batch_size):
    """
    Processes batches of users, filtering those over age 25.
    Prints each user dict one by one.
    """
    for batch in stream_users_in_batches(batch_size):  # loop #2
        for user in batch:  # loop #3
            if int(user["age"]) > 25:
                print(user)
