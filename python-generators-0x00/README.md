# Python Generators – 0x00

This project demonstrates how to set up a MySQL database, seed it with data from a CSV file, and prepare it for streaming rows using Python generators.

## Files
- **seed.py**: Contains helper functions to connect to MySQL, create the database `ALX_prodev`, create the `user_data` table, and insert CSV data.
- **0-main.py**: Entry script to run the setup.
- **user_data.csv**: Sample dataset with user info.

## Database Schema
**Database:** `ALX_prodev`  
**Table:** `user_data`
- `user_id` (UUID, Primary Key, Indexed)
- `name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, NOT NULL)
- `age` (DECIMAL, NOT NULL)

## How to Run
1. Install MySQL and `mysql-connector-python`:
   ```bash
   pip install mysql-connector-python
2. Update MySQL `user` and `password` in **seed.py** if needed.  

3. Run the script:
   ```bash
   ./0-main.py
4. It will:
    Create database ALX_prodev
    Create user_data table
    Insert data from user_data.csv
    Show first 5 rows