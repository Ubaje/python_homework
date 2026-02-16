import sqlite3

DB_PATH = "../db/magazines.db"

#TASK 1
def connect_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = 1")
        return conn
    except sqlite3.Error as e:
        print("Database connection error:", e)
        return None

#TASK 2
def create_tables(conn):
    try:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id),
            UNIQUE(subscriber_id, magazine_id)
        )
        """)

    except sqlite3.Error as e:
        print("Error creating tables:", e)

#Task 3
def add_publisher(conn, name):
    try:
        conn.execute(
            "INSERT OR IGNORE INTO publishers (name) VALUES (?)",
            (name,)
        )
    except sqlite3.Error as e:
        print("Error adding publisher:", e)


def add_magazine(conn, name, publisher_name):
    try:
        publisher_id = conn.execute(
            "SELECT publisher_id FROM publishers WHERE name = ?",
            (publisher_name,)
        ).fetchone()

        if publisher_id:
            conn.execute(
                "INSERT OR IGNORE INTO magazines (name, publisher_id) VALUES (?, ?)",
                (name, publisher_id[0])
            )
    except sqlite3.Error as e:
        print("Error adding magazine:", e)


def add_subscriber(conn, name, address):
    try:
        existing = conn.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (name, address)
        ).fetchone()

        if not existing:
            conn.execute(
                "INSERT INTO subscribers (name, address) VALUES (?, ?)",
                (name, address)
            )
    except sqlite3.Error as e:
        print("Error adding subscriber:", e)


def add_subscription(conn, subscriber_name, address, magazine_name, expiration_date):
    try:
        subscriber_id = conn.execute(
            "SELECT subscriber_id FROM subscribers WHERE name = ? AND address = ?",
            (subscriber_name, address)
        ).fetchone()

        magazine_id = conn.execute(
            "SELECT magazine_id FROM magazines WHERE name = ?",
            (magazine_name,)
        ).fetchone()

        if subscriber_id and magazine_id:
            conn.execute("""
                INSERT OR IGNORE INTO subscriptions
                (subscriber_id, magazine_id, expiration_date)
                VALUES (?, ?, ?)
            """, (subscriber_id[0], magazine_id[0], expiration_date))

    except sqlite3.Error as e:
        print("Error adding subscription:", e)

#Task 4
def run_queries(conn):
    print("\n--- All Subscribers ---")
    for row in conn.execute("SELECT * FROM subscribers"):
        print(row)

    print("\n--- All Magazines (sorted by name) ---")
    for row in conn.execute("SELECT * FROM magazines ORDER BY name"):
        print(row)

    print("\n--- Magazines by Publisher: A ---")
    for row in conn.execute("""
        SELECT magazines.name
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.publisher_id
        WHERE publishers.name = ?
    """, ("A",)):
        print(row)


def main():
    #Task 1
    conn = connect_db()
    if not conn:
        return

    #Task 2
    create_tables(conn)

    # Task 3
    add_publisher(conn, "A")
    add_publisher(conn, "B")
    add_publisher(conn, "C")

    add_magazine(conn, "AARP The Magazine", "A")
    add_magazine(conn, "Costco Connection", "C")
    add_magazine(conn, "Better Homes & Gardens", "B")

    add_subscriber(conn, "SpongeBob SquarePants", "123 Main St")
    add_subscriber(conn, "Patrick Star", "456 Oak Ave")
    add_subscriber(conn, "SpongeBob SquarePants", "789 Pine Rd")
    add_subscriber(conn, "SpongeBob SquarePants", "789 Pine Rd")

    add_subscription(conn, "SpongeBob SquarePants", "123 Main St", "AARP The Magazine", "2026-01-01")
    add_subscription(conn, "Patrick Star", "456 Oak Ave", "Costco Connection", "2025-12-31")
    add_subscription(conn, "SpongeBob SquarePants", "789 Pine Rd", "Better Homes & Gardens", "2024-06-30")

    conn.commit()

    #Task 4
    run_queries(conn)

    conn.close()


if __name__ == "__main__":
    main()
