import pandas as pd
import sqlite3

users=pd.read_csv('users.csv')
orders=pd.read_csv('orders.csv')
print(orders.head())

conn=sqlite3.connect('ecommerce.db')
users.to_sql('users',conn, if_exists='replace', index=False)
orders.to_sql('orders',conn, if_exists='replace', index=False)


print("Users:" , conn.execute("SELECT COUNT(*) FROM users").fetchone()[0])
print("Orders:" , conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0])


cursor = conn.cursor()
print("\nTop 5 users")
cursor.execute("SELECT *FROM users LIMIT 5")
for row in cursor.fetchall():
    print(row)

print("\nTop 5 orders:")
cursor.execute("SELECT *FROM orders LIMIT 5")
for row in cursor.fetchall():
    print(row)

print(" \nTotal users")
cursor.execute("SELECT COUNT(*) FROM users")
print(cursor.fetchone()[0])

print(" \nTotal orders")
cursor.execute("SELECT COUNT(*) FROM orders")
print(cursor.fetchone()[0])

print("\n Cancelled Orders")
cursor.execute("SELECT * FROM orders WHERE status='Cancelled'")
for row in cursor.fetchall():
    print(row)

print("\n Join Uers and Orders (Top 5):")
cursor.execute("SELECT u.first_name, o.gender , o.status FROM users u JOIN orders o ON u.created_at=o.created_at LIMIT 5")
for row in cursor.fetchall():
    print(row)




conn.commit()
conn.close()

print("Data  loaded Sucessfully")
print("SQL queries Executed succesfully")


