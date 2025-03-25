import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import random

# Database connection parameters
DB_NAME = "yourdatabase"
DB_USER = "yourusername"
DB_PASSWORD = "mysecretpassword"
DB_HOST = "localhost"
DB_PORT = "5432"

# Sample data
activity_types = ["Meeting", "Coding", "Review", "Testing", "Design"]
descriptions = [
    "Discuss project requirements",
    "Implement new feature",
    "Code review session",
    "Test new release",
    "Design system architecture"
]

def generate_random_date():
    """Generate a random date within the last 30 days."""
    today = datetime.now()
    random_days = random.randint(0, 30)
    return today - timedelta(days=random_days)

def insert_activity_data(conn, num_records=100):
    """Insert random activity data into the activities table."""
    with conn.cursor() as cur:
        for _ in range(num_records):
            employee_id = random.randint(1, 10)  # Assuming you have 10 employees
            activity_type = random.choice(activity_types)
            activity_date = generate_random_date()
            description = random.choice(descriptions)

            cur.execute(
                sql.SQL("INSERT INTO activities (employee_id, activity_type, activity_date, description) VALUES (%s, %s, %s, %s)"),
                (employee_id, activity_type, activity_date, description)
            )
        conn.commit()

def main():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    try:
        insert_activity_data(conn)
        print("Data inserted successfully.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
