#!/usr/bin/python3
"""
2-lazy_paginate.py - Lazy loading paginated data from user_data
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily fetches pages of users from user_data.
    Uses only one loop and yields each page when needed.
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
