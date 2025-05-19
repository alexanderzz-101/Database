from flask import Flask, render_template, request, redirect, url_for
from db import get_connection

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return render_template('home.html')

# Vendors page
@app.route('/vendors')
def vendors():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Vendors")
    vendors = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('vendors.html', vendors=vendors)

# Add vendor
@app.route('/vendor/add', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        stall_number = request.form['stall_number']
        
        db = get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO Vendors (name, contact_info, stall_number) VALUES (%s, %s, %s)",
                       (name, contact_info, stall_number))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('vendors'))
    
    return render_template('add_vendor.html')

# Edit vendor
@app.route('/vendor/edit/<int:vendor_id>', methods=['GET', 'POST'])
def edit_vendor(vendor_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        stall_number = request.form['stall_number']
        
        cursor.execute("""
            UPDATE Vendors
            SET name = %s, contact_info = %s, stall_number = %s
            WHERE vendor_id = %s
        """, (name, contact_info, stall_number, vendor_id))
        
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('vendors'))

    cursor.execute("SELECT * FROM Vendors WHERE vendor_id = %s", (vendor_id,))
    vendor = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit_vendor.html', vendor=vendor)

# Delete vendor
@app.route('/vendor/delete/<int:vendor_id>')
def delete_vendor(vendor_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Vendors WHERE vendor_id = %s", (vendor_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('vendors'))

# Products page
@app.route('/products')
def products():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('products.html', products=products)

# Add product
@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        name = request.form['name']
        category = request.form['category']
        unit = request.form['unit']
        
        db = get_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Products (vendor_id, name, category, unit) VALUES (%s, %s, %s, %s)",
            (vendor_id, name, category, unit)
        )
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

# Edit product
@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    db = get_connection()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        name = request.form['name']
        category = request.form['category']
        unit = request.form['unit']

        cursor.execute("""
            UPDATE Products
            SET vendor_id = %s, name = %s, category = %s, unit = %s
            WHERE product_id = %s
        """, (vendor_id, name, category, unit, product_id))
        
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('products'))

    cursor.execute("SELECT * FROM Products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template('edit_product.html', product=product)

# Delete product
@app.route('/product/delete/<int:product_id>')
def delete_product(product_id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Products WHERE product_id = %s", (product_id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('products'))

# Inventory page
@app.route('/inventory')
def inventory():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.name, i.quantity_available, p.unit
        FROM Inventory i
        JOIN Products p ON i.product_id = p.product_id
    """)
    inventory_items = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('inventory.html', inventory=inventory_items)

# Orders page
@app.route('/orders')
def orders():
    db = get_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.order_id, o.order_date, o.status, 
               SUM(oi.quantity_sold * p.price) AS total_amount
        FROM Orders o
        JOIN Order_Items oi ON o.order_id = oi.order_id
        JOIN Products p ON oi.product_id = p.product_id
        GROUP BY o.order_id
        ORDER BY o.order_date DESC
    """)
    orders = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
