import sqlite3
import pandas as pd

DB_PATH = "../db/lesson.db"

def main():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        line_items.line_item_id,
        line_items.quantity,
        products.product_id,
        products.product_name,
        products.price
    FROM line_items
    JOIN products
        ON line_items.product_id = products.product_id
    """

    df = pd.read_sql_query(query, conn)

    print(df.head(5), end="\n\n")

    df['total'] = df['quantity'] * df['price']

    print(df.head(5), end="\n\n")

    summary = (df.groupby('product_id').agg({'line_item_id': 'count','total': 'sum','product_name': 'first'}).reset_index())

    print(summary.head(), end="\n\n")

    summary = summary.sort_values(by='product_name')

    summary.to_csv("order_summary.csv", index=False)

    conn.close()


if __name__ == "__main__":
    main()
