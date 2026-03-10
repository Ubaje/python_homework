import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('../db/lesson.db')

query = """
SELECT last_name, SUM(price * quantity) AS revenue
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
JOIN line_items l ON o.order_id = l.order_id
JOIN products p ON l.product_id = p.product_id
GROUP BY e.employee_id;
"""

df = pd.read_sql_query(query, conn)
conn.close()

df.plot(x='last_name', y='revenue', kind='bar', color='steelblue', title='Revenue by Employee')
plt.xlabel('Employee')
plt.ylabel('Revenue ($)')
plt.tight_layout()
plt.show()