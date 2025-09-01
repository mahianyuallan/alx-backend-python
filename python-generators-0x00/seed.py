#!/usr/bin/python3
"""
seed.py - Setup MySQL database ALX_prodev and populate user_data table.
"""

import mysql.connector
from mysql.connector import Error
import uuid
import csv


def connect_db():
    """Connects to the MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # change if using a different MySQL user
            password="root"     # change to your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Creates database ALX_prodev if it doesn’t exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """Connects to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="ALX_prodev"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection):
    """Creates user_data table if it doesn’t exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """Inserts data into user_data table from CSV if not already present."""
    try:
        cursor = connection.cursor()

        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                # avoid duplicates
                cursor.execute(
                    "SELECT * FROM user_data WHERE email = %s",
                    (email,)
                )
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (user_id, name, email, age)
                    )

        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
