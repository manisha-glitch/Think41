from flask import Flask ,jsonify, abort
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ecommerce.db')
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/customers', methods=['GET'])
def get_all_customers():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])

@app.route('/customers/<int:id>',methods=['GET'])
def get_customer(id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',(id)).fetchone()
    if user is None:
        conn.close()
        abort(404,description="Customer not found")

        order_count=conn.execute('SELECT COUNT(*) FROM orders WHERE id=?',(id)).fetchone()[0]
        conn.close()

        user_data = dict(user)
        user_data['order_count']=order_count

        return josnify(user_data)
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':str(error)}),404



@app.route('/customers/<int:user_id>/orders', methods=['GET'])
def get_customer_orders(user_id):
    conn = get_db_connection()
    
    # First check if customer exists
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if user is None:
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    # Fetch all orders for that user
    orders = conn.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    if not orders:
        return jsonify({"message": "No orders found for this customer"}), 200

    return jsonify([dict(order) for order in orders])

if __name__ =='__main__':
    app.run(debug=True)