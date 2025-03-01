import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    # Insert sample data
    c.execute("INSERT INTO orders (order_id, delivery_date, distance) VALUES ('order1', '2023-10-01', 50)")
    c.execute("INSERT INTO orders (order_id, delivery_date, distance) VALUES ('order2', '2023-10-02', 30)")
    c.execute("INSERT INTO orders (order_id, delivery_date, distance) VALUES ('order3', '2023-10-03', 70)")
    c.execute("INSERT INTO orders (order_id, delivery_date, distance) VALUES ('order4', '2023-10-04', 20)")
    c.execute("INSERT INTO orders (order_id, delivery_date, distance) VALUES ('order5', '2023-10-05', 90)")
    conn.commit()
    conn.close()
    print("Sample data inserted")

if __name__ == "__main__":
    insert_sample_data()