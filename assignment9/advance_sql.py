import sqlite3
from datetime import datetime

DB_PATH = "../db/lesson.db"


def open_connection():
    # Let us manage transactions explicitly with BEGIN and COMMIT
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = 1")
    return conn


def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def scalar_int(conn: sqlite3.Connection, sql: str, params: tuple = ()):
    row = conn.execute(sql, params).fetchone()
    if row is None:
        raise ValueError(f"No row returned for query: {sql.strip()}")
    return int(row[0])

# TASK 1
def task1(conn: sqlite3.Connection):
    print_section("Task 1: Find the total price of each of the first 5 orders.")

    sql = """
        SELECT
            o.order_id,
            SUM(p.price * li.quantity) AS total_price
        FROM orders AS o
        JOIN line_items AS li
            ON o.order_id = li.order_id
        JOIN products AS p
            ON li.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5;
    """
    rows = conn.execute(sql).fetchall()
    for r in rows:
        print(f"order_id: {r['order_id']}  total price: {r['total_price']:.2f}")

# TASK 2
def task2(conn: sqlite3.Connection):
    print_section("Task 2  For each customer, find the average price of their orders")

    # Average of per-order totals, per customer
    sql = """
        SELECT
            c.customer_id,
            c.customer_name,
            AVG(order_totals.total_price) AS avg_order_total
        FROM customers AS c
        LEFT JOIN (
            SELECT
                o.customer_id,
                o.order_id,
                SUM(p.price * li.quantity) AS total_price
            FROM orders AS o
            JOIN line_items AS li
                ON li.order_id = o.order_id
            JOIN products AS p
                ON p.product_id = li.product_id
            GROUP BY o.customer_id, o.order_id
        ) AS order_totals
            ON order_totals.customer_id = c.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY c.customer_id;
    """

    rows = conn.execute(sql).fetchall()
    for r in rows:
        avg_val = r["avg_order_total"]
        if avg_val is None:
            print(f"{r['customer_name']}  average total price None")
        else:
            print(f"{r['customer_name']}  average total price {avg_val:.2f}")


# TASK 3
def task3(conn: sqlite3.Connection):
    print_section("Task 3  Create an order for Perez and Sons")

    customer_id = scalar_int(
        conn,
        "SELECT customer_id FROM customers WHERE customer_name = ?;",
        ("Perez and Sons",),
    )
    employee_id = scalar_int(
        conn,
        "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?;",
        ("Miranda", "Harris"),
    )

    product_rows = conn.execute(
        """
        SELECT product_id
        FROM products
        ORDER BY price ASC
        LIMIT 5;
        """
    ).fetchall()
    product_ids = [int(r[0]) for r in product_rows]
    if len(product_ids) < 5:
        raise ValueError("Expected at least 5 products in the products table")

    order_date = datetime.now().date().isoformat()

    # One explicit transaction for the whole operation
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            """
            INSERT INTO orders (customer_id, employee_id, date)
            VALUES (?, ?, ?);
            """,
            (customer_id, employee_id, order_date),
        )
        order_id = int(conn.execute("SELECT last_insert_rowid();").fetchone()[0])

        for product_id in product_ids:
            conn.execute(
                """
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
                """,
                (order_id, product_id, 10),
            )

        conn.commit()
    except Exception:
        conn.rollback()
        raise

    print(f"Created order_id {order_id}")

    rows = conn.execute(
        """
        SELECT
            li.line_item_id,
            li.quantity,
            p.product_name
        FROM line_items AS li
        JOIN products AS p
            ON p.product_id = li.product_id
        WHERE li.order_id = ?
        ORDER BY li.line_item_id;
        """,
        (order_id,),
    ).fetchall()

    for r in rows:
        print(f"line_item_id {r['line_item_id']}  quantity {r['quantity']}  product {r['product_name']}")


def task4(conn: sqlite3.Connection):
    print_section("Task 4  Employees with more than 5 orders")

    sql = """
        SELECT
            e.employee_id,
            e.first_name,
            e.last_name,
            COUNT(o.order_id) AS order_count
        FROM employees AS e
        JOIN orders AS o
            ON e.employee_id = o.employee_id
        GROUP BY e.employee_id
        HAVING COUNT(o.order_id) > 5
        ORDER BY order_count DESC, e.employee_id ASC;
    """
    rows = conn.execute(sql).fetchall()
    for r in rows:
        print(
            f"employee_id {r['employee_id']}  {r['first_name']} {r['last_name']}  orders {r['order_count']}"
        )

def main():
    conn = open_connection()
    try:
        task1(conn)
        task2(conn)
        task3(conn)
        task4(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()